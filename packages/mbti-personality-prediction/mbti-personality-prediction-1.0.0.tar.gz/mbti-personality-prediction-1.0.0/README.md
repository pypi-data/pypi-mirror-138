# MBTIPersonalityPrediction

It predicts MBTI personality type from one's writing style through Linguistic Inquiry and Word Count.

## Installation

Use the package manager [pip][pip-url] to install mbti-personality-prediction.

```bash
pip install mbti-personality-prediction
```

## Usage

```python
# Imports the MBTIPersonalityPrediction class from the mbti_personality_prediction package
from mbti_personality_prediction import MBTIPersonalityPrediction

# Instantiates the MBTI model
app = MBTIPersonalityPrediction()

# Predicts the MBTI personality type based on the writing style of the text input
mbti_type = app.predict_personality('Insert your writing here. It is recommended that the writing is at least a paragraph for a more accurate prediction.')
```

## License

[MIT][mit-license]

[pip-url]: https://pip.pypa.io/en/stable/
[mit-license]: https://choosealicense.com/licenses/mit/
