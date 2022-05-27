class WebBrowser:
    def __init__(self):
        self.chrome_options = Options()

    def set_options(self, **args):
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.binary_location = "/usr/bin/brave"
        self.chrome_options.add_argument("--kiosk")  # To open Brave in Full Screen

    def login_to_platform(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://candidature.1337.ma/users/sign_in")
        self.driver.find_element(By.ID, "user_email").send_keys(
            get_credentials()["email"]
        )
        self.driver.find_element(By.ID, "user_password").send_keys(
            get_credentials()["password"]
        )
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "div a.cc-btn.cc-allow",
                )
            )
        ).click()
        self.driver.find_element(
            By.XPATH, '//*[@id="new_user"]/div[2]/div[3]/input'
        ).click()

    def is_site_changed(self):
        b = self.driver.find_element(By.CSS_SELECTOR, "#subs-content > p").text
        return "No Piscines are currently open." in b


def get_ip_informations() -> list[str, str, str]:
    """
    Returns:
        list[str, str, str]: [ip, city, country]
    """
    endpoint = "https://ipinfo.io/json"
    response = requests.get(endpoint, verify=True)
    if response.status_code != 200:
        return "Status:", response.status_code, "Problem with the request. Exiting."
    data = response.json()
    return [data["ip"], data["city"], data["country"]]