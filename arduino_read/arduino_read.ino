#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

// Uncomment this line to use long range mode. This
// increases the sensitivity of the sensor and extends its
// potential range, but increases the likelihood of getting
// an inaccurate reading because of reflections from objects
// other than the intended target. It works best in dark
// conditions.

//#define LONG_RANGE


// Uncomment ONE of these two lines to get
// - higher speed at the cost of lower accuracy OR
// - higher accuracy at the cost of lower speed

//#define HIGH_SPEED
//#define HIGH_ACCURACY

const char id[] = "aaa"; //change the ID

const char id_get = 'i'; //id

const char distance_get = 'g'; //get

const int init_pin = 9;
//pin 9 to pin INT (on CJMCU 530 sensor module), it is required for the sensor to start working
//connect like usual i2c

const int check_times = 10;

void setup()
{
  Serial.begin(38400);
  
  pinMode(init_pin,OUTPUT);
  digitalWrite(init_pin, HIGH);
  delay(1);
  digitalWrite(init_pin,LOW);

  Wire.begin();

  sensor.init();Serial.print("done");
  sensor.setTimeout(500);

#if defined LONG_RANGE
  // lower the return signal rate limit (default is 0.25 MCPS)
  sensor.setSignalRateLimit(0.1);
  // increase laser pulse periods (defaults are 14 and 10 PCLKs)
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
#endif

#if defined HIGH_SPEED
  // reduce timing budget to 20 ms (default is about 33 ms)
  sensor.setMeasurementTimingBudget(20000);
#elif defined HIGH_ACCURACY
  // increase timing budget to 200 ms
  sensor.setMeasurementTimingBudget(200000);
#endif

}


int read_distance() {
  int distance = sensor.readRangeSingleMillimeters();
  
  if (sensor.timeoutOccurred()) {
    return 0; 
  }
  
  if (distance > 8000) {
    return 1300;
  }
  return distance;
}
void respond_distance() {
  int divide = 0;
  int number = 0;
  int temp_number;
  for (int i = 0; i < check_times; ++i) {
    temp_number = read_distance();
    if (temp_number != 0) {
      number = number + temp_number;
      divide = divide + 1;
    }
    temp_number = 0;
  }
  Serial.println(number/divide);
}
void respond_id() {
  Serial.println(id);
}


void loop() {
  if (Serial.available() > 0) {
    char incoming = Serial.read();

    if (incoming == id_get) {
      respond_id();
    }
    if (incoming == distance_get) {
      respond_distance();
    }
  }
}

