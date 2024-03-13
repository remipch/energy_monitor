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

// Only used with "bufferized" mode
static const int MEASURE_BUFFER_SIZE= 70; // Warning : high values cause out of memory instability
int measure_buffer[MEASURE_BUFFER_SIZE][ANALOG_PINS_COUNT];

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
  Serial.println(F("# rms_measure.ino"));
  Serial.println(F("# Ready, waiting command..."));
}

// Convert analog input to millivolts
int inputVoltage(long input) {
  return (input * 5000) / 1023;
}

void printBufferizedVoltage() {
  // Bufferize measure as fast as possible
  unsigned long start_time_ms = millis();
  for(int i=0;i<MEASURE_BUFFER_SIZE;i++) {
    for(int j=0;j<ANALOG_PINS_COUNT;j++) {
      measure_buffer[i][j] = analogRead(ANALOG_PINS[j]);
    }
  }
  unsigned long end_time_ms = millis();

  // Print timing data
  Serial.print(F("# duration(ms): "));
  Serial.println(end_time_ms - start_time_ms);

  // Convert to mV and print bufferized measures
  Serial.println(F("# A7(mV) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV)"));
  for(int i=0;i<MEASURE_BUFFER_SIZE;i++) {
    for(int j=0;j<ANALOG_PINS_COUNT;j++) {
      Serial.print(inputVoltage(measure_buffer[i][j]));
      Serial.print(separator);
    }
    Serial.println();
  }
  Serial.println();
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
      Serial.print(F("# Separator: \""));
      Serial.print(separator);
      Serial.println("\"");
    }
    else if (command == "b") { // Bufferized voltages
      mode = IDLE;
      Serial.println(F("# Bufferized input"));
      printBufferizedVoltage();
    }
    else if (command == "u") { // Unfiltered voltages
      mode = UNFILTERED_VOLTAGE;
      Serial.println(F("# Unfiltered input"));
      Serial.println(F("# time(ms) A7(mV) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV)"));
    }
    else if (command.startsWith("r")) { // RMS voltages
      mode = RMS_VOLTAGE;
      measure_duration_ms = command.substring(1).toInt();
      measure_duration_ms = constrain(measure_duration_ms, MIN_MEASURE_DURATION_MS,  MAX_MEASURE_DURATION_MS);
      Serial.print(F("# RMS voltage, measure_duration: "));
      Serial.print(measure_duration_ms);
      Serial.println(F(" ms"));
      Serial.println(F("# start_time(ms) end_time(ms) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV) samples_count"));
    }
    else {
      mode = IDLE;
      Serial.print(F("# Unknown command: \""));
      Serial.print(command);
      Serial.println(F("\" -> STOP"));
    }
  }

  if(mode==UNFILTERED_VOLTAGE) {
    printUnfilteredVoltage();
  }
  else if(mode==RMS_VOLTAGE) {
    printRmsVoltage(measure_duration_ms);
  }
}
