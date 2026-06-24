import os, requests, time

TOKEN = os.environ["BOT_TOKEN"]
BASE  = f"https://api.telegram.org/bot{TOKEN}"

def answer_pcq(pcq_id):
    requests.post(f"{BASE}/answerPreCheckoutQuery",
                  json={"pre_checkout_query_id": pcq_id, "ok": True}, timeout=8)

def main():
    offset = 0
    print("Bot started", flush=True)
    while True:
        try:
            r = requests.get(f"{BASE}/getUpdates",
                             params={"offset": offset, "timeout": 30,
                                     "allowed_updates": ["pre_checkout_query", "message"]},
                             timeout=35)
            for u in r.json().get("result", []):
                offset = u["update_id"] + 1
                if "pre_checkout_query" in u:
                    pcq = u["pre_checkout_query"]
                    print(f"PCQ from {pcq['from']['id']}", flush=True)
                    answer_pcq(pcq["id"])
                elif "message" in u and u["message"].get("successful_payment"):
                    sp = u["message"]["successful_payment"]
                    uid = u["message"]["from"]["id"]
                    print(f"Paid {sp['total_amount']} XTR from {uid}", flush=True)
        except Exception as e:
            print(f"Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    main()
