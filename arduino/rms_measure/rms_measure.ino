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
static const int MEASURE_BUFFER_SIZE = 800; // Warning : high values cause out of memory instability
int measure_buffer[MEASURE_BUFFER_SIZE];

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

void printBufferizedVoltage(int input_mask) {
  Serial.println(F("# Bufferized input"));

  int input_to_read[ANALOG_PINS_COUNT];
  int input_count = 0;
  Serial.print("#time(us)");
  for(int i=0;i<ANALOG_PINS_COUNT;i++) {
    int pin_bit = ANALOG_PINS_COUNT - 1 - i; // Because stored in reverse order in ANALOG_PINS
    if(input_mask&(1<<pin_bit)) {
      input_to_read[input_count++] = i;
      Serial.print(separator);
      Serial.print("A");
      Serial.print(pin_bit);
      Serial.print("(mV)");
    }
  }

  int measure_count = input_count * (MEASURE_BUFFER_SIZE / input_count);

  // Bufferize measures as fast as possible
  unsigned long start_time_us = micros();
  for(int i=0;i<measure_count;i++) {
    measure_buffer[i] = analogRead(ANALOG_PINS[input_to_read[i%input_count]]);
  }
  unsigned long end_time_us = micros();

  // Convert to mV and print bufferized measures
  for(int i=0;i<measure_count;i++) {
    if((i%input_count)==0) {
      Serial.println();
      Serial.print((i * (end_time_us-start_time_us))/MEASURE_BUFFER_SIZE);
    }
    Serial.print(separator);
    Serial.print(inputVoltage(measure_buffer[i]));
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
    else if (command.startsWith("b")) { // Bufferized voltages
      String arg = command.substring(1);
      mode = IDLE;
      int input_mask = (arg.length()>0) ? arg.toInt() : 0xFF;
      printBufferizedVoltage(input_mask);
    }
    else if (command == "u") { // Unfiltered voltages
      mode = UNFILTERED_VOLTAGE;
      Serial.println(F("# Unfiltered input"));
      Serial.println(F("#time(ms) A7(mV) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV)"));
    }
    else if (command.startsWith("r")) { // RMS voltages
      mode = RMS_VOLTAGE;
      measure_duration_ms = command.substring(1).toInt();
      measure_duration_ms = constrain(measure_duration_ms, MIN_MEASURE_DURATION_MS,  MAX_MEASURE_DURATION_MS);
      Serial.print(F("# RMS voltage, measure_duration: "));
      Serial.print(measure_duration_ms);
      Serial.println(F(" ms"));
      Serial.println(F("#start_time(ms) end_time(ms) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV) samples_count"));
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
