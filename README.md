# PoC — Jinja2 + docxtpl contractgenerator

## Quickstart
1. Plaats `overeenkomst_jinja.docx` in dezelfde map als `main.py`.
2. Installeer afhankelijkheden:
   ```bash
   pip install -r requirements.txt
   ```
3. Start de API:
   ```bash
   uvicorn main:app --reload
   ```
4. POST naar `http://localhost:8000/genereer/docx` met JSON body:
   ```json
{
  "context": {
    "makelaar": {
      "naam": "Jan Jansen",
      "biv_nummer": "123456",
      "kantoor": "Immo Jansen",
      "straat": "Stationsstraat",
      "nummer": "12",
      "postcode": "1000",
      "gemeente": "Brussel"
    },
    "verkoper": {
      "natuurlijk_persoon": true,
      "naam": "Piet",
      "voornaam": "Pieter",
      "adres": "Kerkstraat 5, 2000 Antwerpen",
      "contact": {
        "email": "piet@example.com",
        "telefoonnummer": "012 34 56 78"
      }
    },
    "koper": {
      "natuurlijk_persoon": true,
      "voor_zichzelf": true,
      "naam": "Klara",
      "voornaam": "Klaartje",
      "adres": "Laan 10, 3000 Leuven",
      "contact": {
        "email": "klara@example.com",
        "telefoonnummer": "098 76 54 32"
      }
    },
    "goed": {
      "straat": "Dorpsplein",
      "nummer": "1",
      "postcode": "8500",
      "gemeente": "Kortrijk",
      "land": "België",
      "aard": "Woning"
    },
    "roerende_goederen": {
      "geen": true,
      "inbegrepen": false
    },
    "genot": {
      "niet_verhuurd": true
    },
    "prijs": {
      "totaal": 350000,
      "voorschot": {
        "bedrag": 35000,
        "overschrijving": true,
        "als_voorschot": true
      },
      "saldo_koopsom": 315000
    },
    "epc": {
      "code": "2025-EP-000001",
      "datum": "2025-10-01"
    },
    "asbestattest": {
      "aanwezig": true,
      "code": "OVAM-123",
      "datum": "2025-09-20",
      "veilig": true
    }
  }
}
   ```

## Template tips
- Boolean velden:
  ```jinja
{% if veld %} ... {% else %} ... {% endif %}
  ```
- Checkbox rendering:
  ```jinja
{% if foo %}☑{% else %}☐{% endif %}
  ```
