const int button1 = 2;
const int button2 = 3; 
const int pot1 = A0;
const int pot2 = A1;
void setup() {
  // put your setup code here, to run once:
pinMode(button1, INPUT);
pinMode(button2, INPUT);
pinMode(pot1, INPUT);
pinMode(pot2, INPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
int read1 = digitalRead(button1);
int read2 = digitalRead(button2);
int amp = analogRead(pot2);
int interval = analogRead(pot1);
Serial.print(read1);
Serial.print(read2);
Serial.print(amp);
Serial.print(interval);
Serial.println();
}
