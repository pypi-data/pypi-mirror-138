# tg-parking-api-client
## telegram_users.basic_operation:
```commandline
    def create_telegram_user(self, user: dict):
        url = self.prepare_url()
        return requests.post(url, json=user).json()
        
    def create_telegram_user(self, user: dict):
        url = self.prepare_url()
        return requests.post(url, json=user).json()

    def get_telegram_user(self, user: dict):
        url = self.prepare_url(f"{user.get('id')}")
        return requests.get(url).json()

    def update_telegram_user(self, user: dict):
        url = self.prepare_url(f"{user.get('id')}")
        return requests.put(url, json=user).json()
```
