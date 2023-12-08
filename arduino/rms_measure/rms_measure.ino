// Analog pins definition
static const uint8_t MIDPOINT_ANALOG_PIN = A7;
static const uint8_t RMS_ANALOG_PINS[] = {A6, A5, A4, A3, A2, A1, A0};
static const uint8_t ANALOG_PINS[] = {A7, A6, A5, A4, A3, A2, A1, A0};
static const int ANALOG_PINS_COUNT = sizeof(ANALOG_PINS)/sizeof(uint8_t);
static const int RMS_ANALOG_PINS_COUNT = sizeof(RMS_ANALOG_PINS)/sizeof(uint8_t);

// Define limits to ensure measure duration is big enough to be meaningful
// and small enough to get a result after a reasonnable time
static const int MIN_MEASURE_DURATION_MS = 40;
static const int MAX_MEASURE_DURATION_MS = 10000;

// 3 modes
enum Mode {
  IDLE,
  UNFILTERED_VOLTAGE, // Measure and print analog voltages as fast as possible
  RMS_VOLTAGE,        // Measure and compute RMS value over a given measure duration
};

Mode mode = IDLE;

String separator = " ";

void setup() {
  Serial.begin(115200);
  Serial.println("# rms_measure.ino");
  Serial.println("# Ready, waiting command...");
}

// Convert analog input to volt
float inputVoltage(int input) {
  return input * (5.0 / 1023.0);
}

void printUnfilteredVoltage() {
  Serial.print(millis());
  for(int i=0;i<ANALOG_PINS_COUNT;i++) {
    Serial.print(separator);
    Serial.print(inputVoltage(analogRead(ANALOG_PINS[i])));
  }
  Serial.println();
}

void printRmsVoltage(unsigned long measure_duration_ms) {
  unsigned long start_time_ms = millis();
  unsigned long end_time_ms = 0;
  long square_sum[RMS_ANALOG_PINS_COUNT] = {0};
  long samples_count = 0;
  do {
    long midpoint = analogRead(MIDPOINT_ANALOG_PIN);
    for(int i=0;i<RMS_ANALOG_PINS_COUNT;i++) {
      square_sum[i] += sq(analogRead(RMS_ANALOG_PINS[i]) - midpoint);
    }
    end_time_ms = millis();
    samples_count++;
  } while((end_time_ms - start_time_ms) < measure_duration_ms);

  Serial.print(start_time_ms);
  Serial.print(separator);
  Serial.print(end_time_ms);
  for(int i=0;i<RMS_ANALOG_PINS_COUNT;i++) {
    Serial.print(separator);
    Serial.print(inputVoltage(sqrt(square_sum[i] / samples_count)));
  }
  Serial.print(separator);
  Serial.print(samples_count);
  Serial.println();
}

void loop() {
  static unsigned long measure_duration_ms = 0;

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.startsWith("s")) { // Separator
      separator = command.substring(1);
      Serial.print("# Separator: \"");
      Serial.print(separator);
      Serial.println("\"");
    }
    else if (command == "u") { // Unfiltered voltages
      mode = UNFILTERED_VOLTAGE;
      Serial.println("# Unfiltered input");
      Serial.println("# time(ms) A7(V) A6(V) A5(V) A4(V) A3(V) A2(V) A1(V) A0(V)");
    }
    else if (command.startsWith("r")) { // RMS voltages
      mode = RMS_VOLTAGE;
      measure_duration_ms = command.substring(1).toInt();
      measure_duration_ms = constrain(measure_duration_ms, MIN_MEASURE_DURATION_MS,  MAX_MEASURE_DURATION_MS);
      Serial.print("# RMS voltage, measure_duration: ");
      Serial.print(measure_duration_ms);
      Serial.println(" ms");
      Serial.println("# start_time(ms) end_time(ms) A6(Vrms) A5(Vrms) A4(Vrms) A3(Vrms) A2(Vrms) A1(Vrms) A0(Vrms) samples_count");
    }
    else {
      mode = IDLE;
      Serial.print("# Unknown command: \"");
      Serial.print(command);
      Serial.println("\" -> STOP");
    }
  }

  if(mode==UNFILTERED_VOLTAGE) {
    printUnfilteredVoltage();
  }
  else if(mode==RMS_VOLTAGE) {
    printRmsVoltage(measure_duration_ms);
  }
}
