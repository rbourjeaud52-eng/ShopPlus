#!/usr/bin/env python3
"""ShopPlus HTTPS smoke checks — safe for production-like pilot environments.

Only GET requests, a stateless quote, invalid input, and anonymous requests
which MUST be denied. Never submits a genuine purchase or a payment.
Requires only Python 3 standard library.
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Route API publiée par le client SDK du déploiement (pas le domaine de la SPA).
BASE_URL = os.environ.get(
    "SHOPPLUS_API_URL",
    "https://api-v2.appdeploy.ai/app/shopplus-haiti-pilote-ub21b4",
).rstrip("/")
TIMEOUT = 12

@dataclass(frozen=True)
class Response:
    code: int
    data: dict

def request(method: str, path: str, data: dict | None = None) -> Response:
    assert BASE_URL.startswith("https://"), "HTTPS obligatoire"
    payload = json.dumps(data).encode("utf-8") if data is not None else None
    req = Request(
        BASE_URL + path,
        data=payload,
        headers={
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if payload is not None else {}),
            "User-Agent": "ShopPlus-GitHub-Free-Release-Check/1.0",
        },
        method=method,
    )
    for attempt in range(3):
        try:
            with urlopen(req, timeout=TIMEOUT) as response:
                code = response.status
                raw = response.read(512 * 1024)
                break
        except HTTPError as e:
            code = e.code
            raw = e.read(512 * 1024)
            if code in (502, 503, 504) and attempt < 2:
                time.sleep(attempt + 1)
                continue
            break
        except (URLError, TimeoutError, OSError) as e:
            if attempt < 2:
                time.sleep(attempt + 1)
                continue
            raise AssertionError(f"{method} {path}: réseau indisponible: {e}") from e
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as e:
        raise AssertionError(
            f"{method} {path}: JSON attendu, reçu HTTP {code}, "
            f"corps: {raw[:180]!r}"
        ) from e
    if not isinstance(obj, dict):
        raise AssertionError(f"{method} {path}: JSON objet requis")
    return Response(code, obj)

def check(predicate: bool, label: str) -> None:
    if not predicate:
        raise AssertionError(label)
    print("  ✓", label, flush=True)

def main() -> int:
    print("ShopPlus — validation HTTPS sans vente ni paiement réels")
    print("Cible:", BASE_URL)

    health = request("GET", "/api/health")
    check(health.code == 200 and health.data.get("ok") is True,
          "API health retourne 200 et ok=true")

    catalog = request("GET", "/api/catalog")
    products = catalog.data.get("products")
    check(catalog.code == 200 and isinstance(products, list) and bool(products),
          "Catalogue démo accessible")

    first = products[0]
    check(
        isinstance(first.get("id"), str)
        and isinstance(first.get("price"), int)
        and first["price"] > 0,
        "Prix de l'article démo valide",
    )

    methods = request("GET", "/api/checkout/methods")
    payments = methods.data.get("methods") or []
    payment_ids = {item.get("id"): item for item in payments}
    check(methods.code == 200 and methods.data.get("livePayments") is False,
          "Encaissements réels explicitement désactivés")
    check(
        all(payment_ids.get(name, {}).get("enabled") is False
            for name in ("moncash", "natcash", "card")),
        "MonCash, NatCash et carte désactivés",
    )
    check(
        payment_ids.get("cod_test", {}).get("testOnly") is True,
        "Paiement à la livraison en simulation seulement",
    )

    quote = request(
        "POST", "/api/demo/quote",
        {"items": [{"id": first["id"], "qty": 2}]},
    )
    check(quote.code == 200
          and quote.data.get("totalHTG") == first["price"] * 2,
          "Devis HTG calculé côté serveur")
    check(
        quote.data.get("kind") == "DEMO_ONLY",
        "Le devis indique DEMO_ONLY et ne crée pas de commande",
    )

    rejected = request(
        "POST", "/api/demo/quote",
        {"items": [{"id": first["id"], "qty": 0}]},
    )
    check(rejected.code == 400,
          "Quantité nulle rejetée par l'API")

    protected_endpoints = [
        ("GET", "/api/orders/test", None),
        ("POST", "/api/orders/test", {
            "requestId": "11111111-1111-4111-8111-111111111111",
            "items": [{"id": first["id"], "qty": 1}],
        }),
        ("GET", "/api/vendor/orders", None),
        ("GET", "/api/admin/overview", None),
        ("POST", "/api/admin/vendors/untrusted-user/approve", {}),
    ]
    for method, path, body in protected_endpoints:
        blocked = request(method, path, body)
        check(blocked.code in (401, 403),
              f"Accès anonyme refusé: {method} {path}")

    print("PASS — Scénarios publics OK. Aucun paiement ni vente effectués.")
    print("NON TESTÉ — sessions connectées, approbations admin, vrai stock, paiements marchands.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1)
