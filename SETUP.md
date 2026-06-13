# Bot Telegram → Vocal (ElevenLabs TTS)

## Cerinte

- Python 3.10 sau mai nou → https://python.org/downloads
- Cont ElevenLabs (planul gratuit = 10.000 caractere/luna) → https://elevenlabs.io

---

## Setup (5 minute)

### 1. Creeaza botul pe Telegram
1. Deschide Telegram si cauta **@BotFather**
2. Trimite `/newbot`
3. Urmeaza instructiunile si copiaza **token-ul** (arata asa: `1234567890:AABBxx...`)

### 2. Ia API key-ul de la ElevenLabs
1. Mergi pe https://elevenlabs.io → logat in cont
2. Click pe poza de profil (dreapta sus) → **Profile**
3. Copiaza **API Key**

### 3. Configureaza `.env`
1. In folderul botului, **copiaza** `.env.example` si **redenumeste-l** in `.env`
2. Deschide `.env` cu Notepad si completeaza:
   ```
   TELEGRAM_TOKEN=token-ul-tau-de-la-botfather
   ELEVENLABS_API_KEY=cheia-ta-elevenlabs
   ```
3. Salveaza

### 4. Porneste botul
Dublu-click pe **`start.bat`**

(Prima oara instaleaza automat pachetele necesare ~30 secunde)

---

## Folosire

| Actiune | Ce faci |
|---|---|
| Text → vocal | Trimite orice text botului |
| Schimba vocea | Trimite `/voice` si alege din lista |
| Vezi vocea activa | Trimite `/currentvoice` |

---

## Limite plan gratuit ElevenLabs

- **10.000 caractere/luna** pe planul gratuit
- ~5-7 minute de audio pe luna
- Daca depasesti, botul iti va spune ca a aparut o eroare

---

## Oprire bot
Apasa `Ctrl+C` in fereastra neagra sau inchide fereastra.
