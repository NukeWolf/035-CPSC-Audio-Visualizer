import board
import neopixel
import time
# for x in range (100):
#     pixels = neopixel.NeoPixel(board.D18,x*3)
#     pixels.fill((255,0,0))
#     time.sleep(0.5)
#     print(x*3)
pixels = neopixel.NeoPixel(board.D18,150)
pixels.fill((155,0,0))
#pixels[0] = (255,255,255)
for x in range(150):
    pixels[x] = (x/150 * 255,255-x/150 * 255,x/150 * 255)
pixels.show()
time.sleep(1);
#pixels.fill((0,0,0));
#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