import time
import board
import digitalio
import pwmio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Adafruit_hid Command Reference
# https://docs.circuitpython.org/projects/hid/en/latest/

#ショートカットの指定1(Windows)
# SW1_SHORTCUT = (Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW) #仮想デスクトップ左切替
# SW2_SHORTCUT = (Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW) #仮想デスクトップ右切替
# SW3_SHORTCUT = (Keycode.CONTROL, Keycode.C) #コピー
# SW4_SHORTCUT = (Keycode.CONTROL, Keycode.V) #ペースト

#ショートカットの指定2(Windows)
# SW1_SHORTCUT = (Keycode.WINDOWS, Keycode.SHIFT, Keycode.S) #範囲指定スクリーンショット
# SW2_SHORTCUT = (Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE) #タスクマネージャーを開く
# SW3_SHORTCUT = (Keycode.WINDOWS, Keycode.ALT, Keycode.D) #日付と時計の表示切り替え
# SW4_SHORTCUT = (Keycode.WINDOWS, Keycode.D) #デスクトップ表示・非表示

#ショートカットの指定3(Windows)
# SW1_SHORTCUT = (Keycode.CONTROL, Keycode.D) #Google Meetマイクミュート切り替え
# SW2_SHORTCUT = (Keycode.CONTROL, Keycode.E) #Google Meetカメラ表示切り替え
# SW3_SHORTCUT = (Keycode.ALT, Keycode.A) #Zoomマイクミュート切り替え
# SW4_SHORTCUT = (Keycode.ALT, Keycode.V) #Zoomカメラ表示切り替え

#ショートカットの指定4(Mac)
# SW1_SHORTCUT = (Keycode.COMMAND, Keycode.A) #全選択
# SW2_SHORTCUT = (Keycode.COMMAND, Keycode.C) #コピー
# SW3_SHORTCUT = (Keycode.COMMAND, Keycode.V) #ペースト
# SW4_SHORTCUT = (Kaeycode.COMMAND,Keycode.SHIFT, Keycode.CONTROL, Keycode.FOUR) #範囲指定スクリーンショット

#ショートカットの指定5(Mac)
# SW1_SHORTCUT = (Keycode.COMMAND, Keycode.KEYPAD_MINUS) #Chrome縮小
# SW2_SHORTCUT = (Keycode.COMMAND, Keycode.KEYPAD_PLUS) #Chrome拡大
# SW3_SHORTCUT = (Keycode.CONTROL, Keycode.COMMAND, Keycode.F) #全画面表示切り替え
# SW4_SHORTCUT = (Keycode.OPTION , Keycode.COMMAND, Keycode.I) #Chrome検証表示切り替え

#ショートカットの指定6(Mac)
# SW1_SHORTCUT = (Keycode.COMMAND, Keycode.D) #Google Meetマイクミュート切り替え
# SW2_SHORTCUT = (Keycode.COMMAND, Keycode.E) #Google Meetカメラ表示切り替え
# SW3_SHORTCUT = (Keycode.COMMAND, Keycode.SHIFT, Keycode.A) #Zoomマイクミュート切り替え
# SW4_SHORTCUT = (Keycode.COMMAND, Keycode.SHIFT, Keycode.V) #Zoomカメラ表示切り替え

#ショートカットの指定7(Mac)
SW1_SHORTCUT = (Keycode.SHIFT, Keycode.OPTION, Keycode.COMMAND, Keycode.T) #Terminal起動
SW2_SHORTCUT = (Keycode.CONTROL, Keycode.COMMAND, Keycode.F) #全画面表示切り替え
SW3_SHORTCUT = (Keycode.OPTION , Keycode.COMMAND, Keycode.I) #Chrome検証表示切り替え
SW4_SHORTCUT = (Keycode.SHIFT, Keycode.COMMAND, Keycode.FOUR) # 範囲選択スクショ

#キーボードデバイスのセットアップ
kbd = Keyboard(usb_hid.devices)

#各スイッチの端子設定
sw1 = digitalio.DigitalInOut(board.GP21)
sw1.direction = digitalio.Direction.INPUT
sw1.pull = digitalio.Pull.UP

sw2 = digitalio.DigitalInOut(board.GP20)
sw2.direction = digitalio.Direction.INPUT
sw2.pull = digitalio.Pull.UP

sw3 = digitalio.DigitalInOut(board.GP19)
sw3.direction = digitalio.Direction.INPUT
sw3.pull = digitalio.Pull.UP

sw4 = digitalio.DigitalInOut(board.GP18)
sw4.direction = digitalio.Direction.INPUT
sw4.pull = digitalio.Pull.UP

#ブザー音の端子設定
buzzer = pwmio.PWMOut(board.GP16, frequency=2300)

#LEDの端子設定
led = pwmio.PWMOut(board.GP25, frequency=5000)

#LED点灯
led.duty_cycle = 1000

#起動時ブザー音
buzzer.duty_cycle = 2000
time.sleep(0.1)
buzzer.duty_cycle = 0
time.sleep(0.1)
buzzer.duty_cycle = 2000
time.sleep(0.1)
buzzer.duty_cycle = 0

#直前のスイッチ状態
old_sw1_value = True
old_sw2_value = True
old_sw3_value = True
old_sw4_value = True

#メインループ
while True:
    # ブザーを鳴らすフラグ初期化
    sound_buzzer = False

    #各スイッチがOFFからONに変わるときを検知
    #kbd.sendの引数はタプルをアンパックして展開
    if sw1.value == False and old_sw1_value == True:
        kbd.send(*SW1_SHORTCUT)
        sound_buzzer = True

    if sw2.value == False and old_sw2_value == True:
        kbd.send(*SW2_SHORTCUT)
        sound_buzzer = True

    if sw3.value == False and old_sw3_value == True:
        kbd.send(*SW3_SHORTCUT)
        sound_buzzer = True

    if sw4.value == False and old_sw4_value == True:
        kbd.send(*SW4_SHORTCUT)
        sound_buzzer = True

    #ブザーはここで鳴らす
    if sound_buzzer == True:
        buzzer.duty_cycle = 2000
        time.sleep(0.1)
        buzzer.duty_cycle = 0

    #直前のスイッチ状態の更新
    old_sw1_value = sw1.value
    old_sw2_value = sw2.value
    old_sw3_value = sw3.value
    old_sw4_value = sw4.value

    #スイッチ入力待ち
    time.sleep(0.01)


