from src.led.led_controller import LedController
from src.led.led_output import MockLEDOutput

def test_play_touch_effect():
    led_config = {
        "led": {
            "count": 24,
            "effects": {
                "touch": {
                    "enabled": True,
                    "file": "touch.csv"
                }
            }
        }
    }

    output = MockLEDOutput()
    controller = LedController(led_config=led_config, output=output)
    controller.play_effect("touch")
    
if __name__ == "__main__":
    test_play_touch_effect()