import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUGGER_ADDRESS = "127.0.0.1:9222"
NORMAL_INTERVAL = 3

AVAILABLE_SELECTOR = "p.txt_ch"
TRAIN_SELECTOR = "h3.txt_bk"
WAITING_TEXT = "예약 대기"
NO_TRAIN_TEXT = "해당 스케줄에 운행하는 열차가 없습니다."

KTX_TAB_SELECTOR = 'button[type="button"][aria-controls="tab_tab_info1"]'


def beep(times=3):
    for _ in range(times):
        print("\a", end="", flush=True)
        time.sleep(0.25)


def body_text(driver):
    try:
        return driver.find_element(By.TAG_NAME, "body").text
    except Exception:
        return ""


def has_available(driver):
    try:
        return any(
            e.text.strip() == "일반실"
            for e in driver.find_elements(By.CSS_SELECTOR, AVAILABLE_SELECTOR)
        )
    except Exception:
        return False


def has_waiting(driver):
    return WAITING_TEXT in body_text(driver)


def has_no_train(driver):
    return NO_TRAIN_TEXT in body_text(driver)


def train_info(driver):
    try:
        for e in driver.find_elements(By.CSS_SELECTOR, TRAIN_SELECTOR):
            text = e.text.strip()
            m = re.search(
                r"(.*?)\s*→\s*(.*?)\s*\((\d{1,2}:\d{2})\s*~\s*(\d{1,2}:\d{2})\)",
                text
            )
            if m:
                return f"{m.group(1).strip()} → {m.group(2).strip()} ({m.group(3)} ~ {m.group(4)})"
            if text:
                return text
    except Exception:
        pass
    return "열차 시간 미확인"


def status(driver):
    if has_available(driver):
        return "available"
    if has_waiting(driver):
        return "waiting"
    if has_no_train(driver):
        return "no_train"
    return "normal"


def click_ktx_tab(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, KTX_TAB_SELECTOR)
        if not buttons:
            print("   KTX/KTX-산천 버튼을 찾지 못했습니다.")
            return False

        button = buttons[0]
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", button
            )
            button.click()
        except (StaleElementReferenceException, WebDriverException):
            buttons = driver.find_elements(By.CSS_SELECTOR, KTX_TAB_SELECTOR)
            if not buttons:
                return False
            driver.execute_script("arguments[0].click();", buttons[0])

        print("   → KTX/KTX-산천 버튼 클릭 완료")
        return True
    except Exception as e:
        print(f"   → 버튼 클릭 실패: {e}")
        return False


def hold_screen(driver, s):
    print()
    print("=" * 60)
    print("★ 일반실 좌석 가능 ★" if s == "available" else "★ 예약 대기 감지 ★")
    print(f"열차: {train_info(driver)}")
    print("자동 조회를 중지하고 현재 화면을 유지합니다.")
    print("종료: Ctrl+C")
    print("=" * 60)
    beep(5)
    while True:
        time.sleep(60)


def connect():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", DEBUGGER_ADDRESS)
    print("[1] Python 실행 성공")
    print("[2] Chrome 원격 디버깅 연결 중...")
    driver = webdriver.Chrome(options=options)
    print("[3] Selenium Chrome 연결 성공!")
    return driver


def main():
    try:
        driver = connect()
    except Exception as e:
        print("Chrome 연결 실패:", e)
        input("Enter를 누르면 종료합니다.")
        return

    print()
    print("=" * 60)
    print("KTX 취소표 감지기 - 3초 KTX 탭 재조회")
    print("=" * 60)
    print("Chrome에서 TEST B 결과 화면을 준비한 뒤 Enter를 누르세요.")
    input("준비 완료 후 Enter: ")
    print("감지를 시작합니다.")
    print("※ 예약/결제 버튼은 자동으로 누르지 않습니다.")
    print()

    try:
        while True:
            s = status(driver)
            now = time.strftime("%H:%M:%S")

            if s == "available":
                wait = WebDriverWait(driver, 10)
                # 1. <div class="inner type02"> 안의 <a title="선택"> 클릭
                select_btn = wait.until(
                   EC.element_to_be_clickable(
                     (By.CSS_SELECTOR, "div.inner.type02 a[title='선택']")
                    )
                 )
                select_btn.click()

                reserv_btn = wait.until(
                 EC.element_to_be_clickable(
            (
                  By.XPATH,
                  "//div[contains(@class, 'reservbtnWrap')]"
                  "//button[normalize-space()='예매' or normalize-space()='예약대기신청']"
            )
        )
    )

                print(f"▶ {reserv_btn.text} 버튼 발견")

                # 버튼이 보이도록 이동
                driver.execute_script(
                 "arguments[0].scrollIntoView({block: 'center'});",
                  reserv_btn
    )

                time.sleep(0.2)

    # 클릭
                reserv_btn.click()

                print(f"▶ {reserv_btn.text} 버튼 클릭 완료")
                print(f"[{now}] ★ 일반실 좌석 가능 감지!")
                print("       " + train_info(driver))
                hold_screen(driver, s)
                
                return

            if s == "waiting":
                print(f"[{now}] ★ 예약 대기 감지!")
                print("       " + train_info(driver))
                hold_screen(driver, s)
                return

            if s == "no_train":
                print(f"[{now}] 해당 스케줄에 운행하는 열차가 없습니다.")

            else:
                print(f"[{now}] 조회 중... 좌석/예약대기 없음")

            time.sleep(NORMAL_INTERVAL)

            s = status(driver)
            if s in ("available", "waiting"):
                hold_screen(driver, s)
                return

            click_ktx_tab(driver)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n사용자가 Ctrl+C로 종료했습니다.")


if __name__ == "__main__":
    main()
