import pytest
import pandas as pd
from src.inducedpolarization.survey import InducedPolarizationSurvey
import os

@pytest.fixture
def sample_survey():
    data = pd.DataFrame({
        "LineNumber": [1, 1, 2, 3],
        "Value": [100, 150, 200, 250]
    })
    return InducedPolarizationSurvey(data)

def test_from_file_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    pd.DataFrame({"LineNumber": [1], "Value": [100]}).to_csv(csv_path, index=False)
    survey = InducedPolarizationSurvey.from_file(str(csv_path))
    assert len(survey.data) == 1

def test_filter_by_line(sample_survey):
    filtered = sample_survey.filter_by_line(1)
    assert len(filtered) == 2
    assert all(filtered["LineNumber"] == 1)

def test_to_csv(sample_survey, tmp_path):
    out_path = tmp_path / "output.csv"
    sample_survey.to_csv(out_path)
    assert os.path.exists(out_path)
    loaded = pd.read_csv(out_path)
    assert len(loaded) == 4