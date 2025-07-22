VALID_CONFIG_YAML = """
boards:
    test:
        board_id: 4
        base_url: "https://test123.atlassian.net/"
        board_name: "Some Fake Scrum Board"
"""

MISSING_BOARDS_YAML = """
not_boards_attribute:
    some_other_thing: true
"""