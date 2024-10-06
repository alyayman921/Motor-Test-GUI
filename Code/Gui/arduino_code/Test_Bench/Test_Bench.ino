/*
Initial configuration must be done while connecting to the arduino
*/
#include <HX711_ADC.h>
#include <Servo.h>
#include <SoftwareSerial.h>

#define HX_DOUT 4
#define HX_SCK 5
#define Throttle_Pot A1
#define ESC_OUT 9
#define Rx 2
#define Tx 3
#define IR 2

HX711_ADC LoadCell(HX_DOUT, HX_SCK);
Servo motor;
SoftwareSerial Bluetooth(Rx, Tx);  // RX, TX


float Calibration_Factor = 450;  //Can not be equal to zero Nan
float Thrust = 0;
int Throttle = 0;
char choice = 'p';
char Get_value = ' ';
long long Calc_Time = 0;
int counter;
char Encoder_Value = 2;
float rpm;


float Calibration_Process();
void Read_Serial();
void Read_Bluetoooth();
void Read_pot();
void Saftey_measure();
void RPM_Calculation();
void setup() {
  Serial.begin(9600);
  Bluetooth.begin(9600);
  Serial.println("---------------------------------------------Starting----------------------------------------------------------");
  Serial.println("---------------------------------------Wait about 2 seconds----------------------------------------------------");
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

  pinMode(Throttle_Pot, INPUT);
  pinMode(IR, INPUT_PULLUP);
  // pinMode(ESC_OUT,OUTPUT);
  motor.attach(ESC_OUT, 1000, 2000);  // 1ms - 2ms pulse width out of 20ms cycle
  Serial.println("Please, Enter how to change thrust p: Potentiometer, b:bluetooth, S:Serial Monitor");
  while (true) {  // Choosing how to vary thrust
    if (Serial.available()) {
      choice = Serial.read();
      Serial.println(choice);
      break;
    }
  }
  Throttle = analogRead(Throttle_Pot);
  while (5 <= Throttle) {  //Saftey measure
    Serial.println("-------------------- Please, Set throttle to Zero----------------------");
    Throttle = analogRead(Throttle_Pot);
  }
  Calc_Time = millis();
  attachInterrupt(digitalPinToInterrupt(IR), RPM_Calculation, RISING);
   Serial.print("Throttle( % )           ");Serial.print("         Thrust( gm )           ");Serial.println("        RPM           ");
}

void loop() {
  switch (choice) {
    case 'b':
      Read_Bluetoooth();
      break;
    case 'B':
      Read_Bluetoooth();
      break;
    case 's':
      Read_Serial();
      break;
    case 'S':
      Read_Serial();
      break;
    default:
      Read_pot();
  }
  int New_Throttle = map(Throttle, 0, 100, 1000, 2000);  // Just for a garabage problem appeared so I made a new variable
  // Serial.println(New_Throttle);
  motor.writeMicroseconds(New_Throttle);
  if (1000 < millis() - Calc_Time) {
    rpm = (float)counter * 60 / Encoder_Value;
    counter = 0;
    Serial.println(rpm);
    Calc_Time = millis();
  }
  if (LoadCell.update()) {
    //Serial.prntln(LoadCell.getData());
    Serial.print(Throttle);Serial.print("                                ");Serial.print(LoadCell.getData());Serial.print("                     ");Serial.println(rpm);
  }
  
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
void Read_Serial() {
  Get_value = Serial.read();
  if ('v' == Get_value) {
    Serial.println("Please, Enter a Value between 0 : 100");
    while (true) {
      if (Serial.available()) {
        Throttle = Serial.parseInt();
        Serial.print("==========================");Serial.println(Throttle);
        if (301 == Throttle) {
          choice = 'p';
          Saftey_measure();
          break;
        } else if (302 == Throttle) {
          choice = 'b';
          Saftey_measure();
          break;
        } else {
          Serial.print(Throttle);
          Serial.println('%');
          if (Throttle > 100) {
            Serial.println("Please, Enter a valid Value between 0 :100");
          } else {
            break;
          }
        }
      }
    }
  }
}
void Read_Bluetoooth() {
  Get_value = Bluetooth.read();
  if ('v' == Get_value) {
    Bluetooth.println('b');
    while (true) {
      if (Bluetooth.available()) {
        Throttle = Bluetooth.parseInt();
        if (301 == Throttle) {
          choice = 'p';
          Saftey_measure();
          break;
        } else if (302 == Throttle) {
          choice = 's';
          Saftey_measure();
          break;
        } else {
          Bluetooth.print(Throttle);
          Bluetooth.println('%');
          if (Throttle > 100) {
            Bluetooth.println("Please, Enter a valid Value between 0 :100");
          } else {
            break;
          }
        }
      }
    }
  }
}
void Read_pot() {
  char Chg = 0;
  if (Serial.available()) {
    Chg = Serial.read();
    if ('s' == Chg) {
      choice = Chg;
      Saftey_measure();
    } else if ('b' == Chg) {
      choice = Chg;
      Saftey_measure();
    } else {
      choice = 'p';
    }

  } else if (Bluetooth.available()) {
    Chg = Bluetooth.read();
    if ('s' == Chg) {
      choice = Chg;
      Saftey_measure();
    } else if ('b' == Chg) {
      choice = Chg;
      Saftey_measure();
    } else {
      choice = 'p';
    }

  } else {
    Throttle = map(analogRead(Throttle_Pot), 0, 1023, 0, 100);
  }
}
void Saftey_measure() {
  while (5 <= Throttle) {  //Saftey measure
    Serial.println("-------------------- Please, Set throttle to Zero----------------------");
    Throttle = map(analogRead(Throttle_Pot), 0, 1023, 0, 100);
    Serial.println(Throttle);
  }
}
void RPM_Calculation() {
  counter = counter + 1;
}