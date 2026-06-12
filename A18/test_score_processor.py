"""
Test suite for ScoreProcessor.

Covers:
  - Happy path: valid file with a numeric score
  - Error path 1: missing file (FileNotFoundError)
  - Error path 2: file with non-numeric content (ValueError)
  - Edge cases: zero, negative numbers, and whitespace-padded values
"""

import os
import tempfile
import pytest
from score_processor import ScoreProcessor

def _make_temp_file(content: str) -> str:
    """Write *content* to a temporary file and return its path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


class TestScoreProcessor:

    def setup_method(self):
        """Create a fresh ScoreProcessor before each test."""
        self.processor = ScoreProcessor()

   

    def test_valid_file_returns_score_multiplied_by_10(self, tmp_path):
        """A file containing '7' should return 70 (7 × 10)."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("7")

        result = self.processor.process_score_file(str(score_file))

        assert result == 70

    def test_valid_file_with_larger_number(self, tmp_path):
        """A file containing '85' should return 850."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("85")

        result = self.processor.process_score_file(str(score_file))

        assert result == 850

    def test_valid_file_with_zero(self, tmp_path):
        """A score of 0 multiplied by 10 should still be 0."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("0")

        result = self.processor.process_score_file(str(score_file))

        assert result == 0

    def test_valid_file_with_negative_number(self, tmp_path):
        """Negative scores are valid integers; -3 × 10 = -30."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("-3")

        result = self.processor.process_score_file(str(score_file))

        assert result == -30

    def test_valid_file_with_whitespace_padding(self, tmp_path):
        """Leading/trailing whitespace around the number should be handled."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("  42  \n")

        result = self.processor.process_score_file(str(score_file))

        assert result == 420

  
    def test_missing_file_raises_file_not_found_error(self):
        """Passing a path that does not exist must raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            self.processor.process_score_file("/nonexistent/path/score.txt")

    def test_missing_file_prints_error_message(self, capsys):
        """The FileNotFoundError handler must print a descriptive error message."""
        with pytest.raises(FileNotFoundError):
            self.processor.process_score_file("/no/such/file.txt")

        captured = capsys.readouterr()
        assert "[ERROR] File not found:" in captured.out
        assert "/no/such/file.txt" in captured.out


    def test_non_numeric_content_raises_value_error(self, tmp_path):
        """A file containing letters instead of a number must raise ValueError."""
        bad_file = tmp_path / "bad.txt"
        bad_file.write_text("abc")

        with pytest.raises(ValueError):
            self.processor.process_score_file(str(bad_file))

    def test_non_numeric_content_prints_error_message(self, tmp_path, capsys):
        """The ValueError handler must print a descriptive error message."""
        bad_file = tmp_path / "bad.txt"
        bad_file.write_text("hello")

        with pytest.raises(ValueError):
            self.processor.process_score_file(str(bad_file))

        captured = capsys.readouterr()
        assert "[ERROR] Invalid data in file:" in captured.out


    def test_cleanup_message_printed_on_success(self, tmp_path, capsys):
        """'File cleanup completed' must appear in output after a successful run."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("5")

        self.processor.process_score_file(str(score_file))

        captured = capsys.readouterr()
        assert "File cleanup completed" in captured.out

    def test_success_message_printed_on_success(self, tmp_path, capsys):
        """'Data processed successfully' must appear after a successful run."""
        score_file = tmp_path / "score.txt"
        score_file.write_text("5")

        self.processor.process_score_file(str(score_file))

        captured = capsys.readouterr()
        assert "Data processed successfully" in captured.out

    def test_cleanup_message_printed_even_on_file_not_found(self, capsys):
        """'File cleanup completed' must appear even when the file is missing."""
        with pytest.raises(FileNotFoundError):
            self.processor.process_score_file("/missing/file.txt")

        captured = capsys.readouterr()
        assert "File cleanup completed" in captured.out

    def test_cleanup_message_printed_even_on_value_error(self, tmp_path, capsys):
        """'File cleanup completed' must appear even when the content is invalid."""
        bad_file = tmp_path / "bad.txt"
        bad_file.write_text("not_a_number")

        with pytest.raises(ValueError):
            self.processor.process_score_file(str(bad_file))

        captured = capsys.readouterr()
        assert "File cleanup completed" in captured.out