#include <HX711_ADC.h>

#define HX_DOUT 4
#define HX_SCK 5

HX711_ADC LoadCell(HX_DOUT, HX_SCK);

float Calibration_Factor = 0;
float Calibration_Process();

void setup() {
  Serial.begin(9600);
  Serial.println("---------------------------------------------Starting----------------------------------------------------------");
  Serial.println("---------------------------------------Wait about 2 seconds-----------------------------------------------");
  LoadCell.begin();
  LoadCell.start(2000, true);
  Serial.print("Do you want to calibrate first? y | n : ");
  while (1) {
    if (Serial.available()) {
      char option = Serial.read();
      if ('y' == option) {
        Calibration_Factor = Calibration_Process();
        LoadCell.setCalFactor(Calibration_Factor);
        break;
      } else {
        Serial.print("\nThx you're calibration factor remains the same = ");
        Serial.println(Calibration_Factor);
        LoadCell.setCalFactor(Calibration_Factor);
        break;
      }
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
}

float Calibration_Process() {
  Serial.println("\n***");
  Serial.println("Start calibration:");
  Serial.println("Place the load cell an a level stable surface.");
  Serial.println("Remove any load applied to the load cell.");
  Serial.println("Send 't' from serial monitor to set the tare offset.");

  while (1) {
    LoadCell.update();
    if (Serial.available() > 0) {
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell.tareNoDelay();
      }
    }
    if (LoadCell.getTareStatus() == true) {
      Serial.println("Tare complete");
      break;
    }
  }
  Serial.println("Now, place your known mass on the loadcell.");
  Serial.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

  float known_mass = 0;
  while (1) {
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        Serial.print("Known mass is: ");
        Serial.println(known_mass);
      }
      break;
    }
  }
  LoadCell.refreshDataSet();                                           //refresh the dataset to be sure that the known mass is measured correct
  float newCalibrationValue = LoadCell.getNewCalibration(known_mass);  //get the new calibration value

  Serial.print("New calibration value has been set to: ");
  Serial.print(newCalibrationValue);

  return newCalibrationValue;
}