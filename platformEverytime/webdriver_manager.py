import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException
class WebDriverManager:
    _instance = None

    def __init__(self):
        self.driver = None
        self.lock = threading.Lock()
        self.default_options = self._create_default_options()

    @staticmethod
    def get_instance():
        if WebDriverManager._instance is None:
            WebDriverManager._instance = WebDriverManager()
        return WebDriverManager._instance

    def _create_default_options(self):
        options = Options()
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless") # 브라우저 띄우지 않음
        options.add_argument("--log-level=3")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        #options.add_argument("--profile-default-content-settings.cookies=1") # 쿠키 허용
        #subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chromeCookie"')
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:8000") # 디버거 주소
        #options.add_experimental_option("prefs", prefs) # 이미지, CSS, 자바스크립트 로드 설정
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        #driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return options

    def get_driver(self, custom_options=None):
        with self.lock:
            if self.driver is None:
                options = self.default_options
                if custom_options:
                    for argument in custom_options.arguments:
                        options.add_argument(argument)
                    for experimental_option, value in custom_options.experimental_options.items():
                        options.add_experimental_option(experimental_option, value)
                try:
                    self.driver = webdriver.Chrome(options=options)
                except SessionNotCreatedException:
                    print("ChromeDriver is not compatible with Chrome Browser")
                    return None
            return self.driver

    def stop_driver(self):
        with self.lock:
            if self.driver is not None:
                self.driver.close()
                self.driver = None
    
    def is_stable(self):
        with self.lock:
            if self.driver is not None:
                try:
                    # Check driver connection by trying to get current URL
                    self.driver.current_url
                    return True
                except Exception as e:
                    print(f"WebDriver is not stable: {str(e)}")
                    return False
            else:
                return False