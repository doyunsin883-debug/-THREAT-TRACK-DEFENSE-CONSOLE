/*
  THREAT-TRACK V5.0
  Ultrasonic + 3 LED + Buzzer + PC Interface
*/

const int TRIG = 2;
const int ECHO = 3;

const int RED_LED = 4;
const int YELLOW_LED = 5;
const int GREEN_LED = 6;
const int BUZZER = 7;

float filteredDistance = 0;
float previousDistance = 0;
float filteredSpeed = 0;

unsigned long previousTime = 0;
bool firstReading = true;

void setLED(bool red, bool yellow, bool green) {
  digitalWrite(RED_LED, red);
  digitalWrite(YELLOW_LED, yellow);
  digitalWrite(GREEN_LED, green);
}

float readDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  unsigned long duration = pulseIn(ECHO, HIGH, 25000UL);

  if (duration == 0) return -1;

  float d = duration * 0.0343 / 2.0;

  if (d < 2 || d > 400) return -1;

  return d;
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  setLED(false, false, false);
  noTone(BUZZER);

  delay(1000);
}

void loop() {
  float rawDistance = readDistance();

  if (rawDistance < 0) {
    setLED(false, false, false);
    noTone(BUZZER);
    firstReading = true;
    filteredSpeed = 0;

    Serial.println("NO_SIGNAL");
    delay(80);
    return;
  }

  unsigned long now = millis();

  if (firstReading) {
    filteredDistance = rawDistance;
    filteredSpeed = 0;
    firstReading = false;
  } else {
    filteredDistance = 0.4 * rawDistance + 0.6 * filteredDistance;

    float dt = (now - previousTime) / 1000.0;

    if (dt > 0) {
      float instantSpeed = (previousDistance - filteredDistance) / dt;
      filteredSpeed = 0.5 * instantSpeed + 0.5 * filteredSpeed;
    }
  }

  previousDistance = filteredDistance;
  previousTime = now;

  float ttc = -1;
  if (filteredSpeed > 10) {
    ttc = filteredDistance / filteredSpeed;
  }

  bool danger = (filteredDistance <= 30) || (ttc > 0 && ttc <= 1.5);
  bool warning = (filteredDistance <= 70) || (ttc > 0 && ttc <= 3.0);

  const char* status = "SAFE";

  if (danger) {
    setLED(true, false, false);
    status = "DANGER";

    if (now % 240 < 120) tone(BUZZER, 1800);
    else noTone(BUZZER);
  }
  else if (warning) {
    setLED(false, true, false);
    status = "WARNING";

    if (now % 900 < 180) tone(BUZZER, 1000);
    else noTone(BUZZER);
  }
  else {
    setLED(false, false, true);
    status = "SAFE";
    noTone(BUZZER);
  }

  // PC-friendly output format
  // distance,speed,ttc,status
  Serial.print(filteredDistance, 1);
  Serial.print(",");
  Serial.print(filteredSpeed, 1);
  Serial.print(",");

  if (ttc > 0) Serial.print(ttc, 2);
  else Serial.print(-1);

  Serial.print(",");
  Serial.println(status);

  delay(80);
}
