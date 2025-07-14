volatile long countLeft = 0;
volatile long countRight = 0;

const float wheelCircumference = 0.212; // in meters
const int countsPerRevolution = 11;

const int leftA = 2; // Encoder A (left motor)
const int leftB = 4; // Encoder B (left motor)
const int rightA = 3; // Encoder A (right motor)
const int rightB = 5; // Encoder B (right motor)

void setup() {
  // put your setup code here, to run once:
  pinMode(leftA, INPUT_PULLUP);
  pinMode(leftB, INPUT_PULLUP);
  pinMode(rightA, INPUT_PULLUP);
  pinMode(rightB, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(leftA), handleLeftEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(rightA), handleRightEncoder, CHANGE);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float leftDistance = (countLeft / (float)countsPerRevolution) * wheelCircumference / 100 / 6 * 5;
  float rightDistance = (countRight / (float)countsPerRevolution) * wheelCircumference / 100 / 6 * 5; 

  Serial.print(leftDistance, 4);
  Serial.print(",");
  Serial.println(rightDistance, 4);

  delay(200);
}

void handleLeftEncoder() {
  // Determine Direction
  if (digitalRead(leftA) == digitalRead(leftB)) {
    countLeft--;
  } else {
    countLeft++;
  }
}

void handleRightEncoder() {
  // Determine Direction
  if (digitalRead(rightA) == digitalRead(rightB)) {
    countRight++;
  } else {
    countRight--;
  }
}
