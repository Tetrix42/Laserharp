// WiringPi-Api einbinden
#include <wiringPi.h>

// C-Standardbibliothek einbinden
#include <stdio.h>

int main() {

  // Starte die WiringPi-Api (wichtig)
  if (wiringPiSetup() == -1)
    return 1;

  // Schalte GPIO 17 (=WiringPi Pin 0) auf Ausgang
  pinMode(0, OUTPUT);

  // Schalte GPIO 24 (=WiringPi Pin 5) auf Eingang
  pinMode(5, INPUT);

  // Dauerschleife
  while(1) {
    // LED immer ausmachen
    digitalWrite(0, 0);

    // GPIO lesen
    if(digitalRead(5)==1) {
      // LED an
      digitalWrite(0, 1);

      // Warte 100 ms
      delay(100);

      // LED aus
      digitalWrite(0, 0);

      // Warte 100 ms
      delay(100);
    }
  }
}
