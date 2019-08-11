These files all make use of adafruit's character lcd library. It is part of the circuitpython bundle. You can find it in the at https://github.com/adafruit/Adafruit_CircuitPython_Bundle


The lcd I am using has the following spec sheet https://cdn-shop.adafruit.com/product-files/399/399+spec+sheet.pdf

| lcd pin       | use           | controler pin|
| ------------- |:-------------:| ------------:|
| 1             | vss           | b            |
| 2             | vdd           | b            |
| 3             | v0            | b            |
| 4             | rs            | 13           |
| 5             | r/w           | gnd          |
| 6             | enable        | 12           |
| 7             | db0           | blank        |
| 8             | db1           | blank        |
| 9             | db2           | blank        |
| 10            | db3           | blank        |
| 11            | db4           | 11           |
| 12            | db5           | 10           |
| 13            | db6           | 9            |
| 14            | db7           | 6            |
| 15            | common annode | usb          |
| 16            | red cathode   | 5            |
| 17            | green cathode | 5            |
| 18            | blue cathode  | 5            |

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |
