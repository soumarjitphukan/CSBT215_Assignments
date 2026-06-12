class ScoreProcessor:

    def process_score_file(self, file_path: str) -> int:
        file = None
        result = None

        try:
            file = open(file_path, "r")
            raw_content = file.read().strip()
            score = int(raw_content)
            result = score * 10

        except FileNotFoundError:
            print(f"[ERROR] File not found: '{file_path}'. "
                  f"Please check that the file exists and the path is correct.")
            raise

        except ValueError:
            print(f"[ERROR] Invalid data in file: '{file_path}'. "
                  f"The file must contain a single integer value, not letters or symbols.")
            raise

        else:
            print("Data processed successfully")

        finally:
            if file is not None:
                file.close()
            print("File cleanup completed")

        return result
