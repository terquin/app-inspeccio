# 🏠 Control Domòtic via Telegram

App web per controlar Home Assistant enviant missatges de Telegram **com a tu** (no com el bot).

## Estructura

```
/
├── index.html          ← L'app web (PWA instal·lable al mòbil)
├── vercel.json         ← Configuració de Vercel
└── api/
    ├── requirements.txt   ← Dependències Python
    ├── send_code.py       ← Demana el codi SMS a Telegram
    ├── verify_code.py     ← Verifica el codi i crea la sessió
    └── send.py            ← Envia comandes com a tu
```

## Com funciona

```
[App web] → [Vercel API] → [Telegram com a TU] → [Home Assistant]
```

1. La primera vegada introdueixes API ID, API Hash i telèfon
2. Telegram t'envia un codi SMS de verificació
3. La sessió es guarda al localStorage del teu mòbil
4. A partir d'aquí els botons envien missatges com si els enviessis tu

## Desplegament a Vercel

1. Fes fork d'aquest repositori a GitHub
2. Ves a [vercel.com](https://vercel.com) i connecta el repositori
3. Desplega (és automàtic)
4. Obre l'app al mòbil i fes el login

## Credencials Telegram

Obtén `API_ID` i `API_HASH` a [my.telegram.org](https://my.telegram.org) → API Development Tools.

> ⚠️ Les credencials es guarden **només al teu dispositiu** (localStorage). No es guarden mai al servidor.
