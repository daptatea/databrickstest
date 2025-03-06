# usage:
# python ./scripts/create_db_question.py --template-id <template-id> --prefix <question-prefix> --text <question-text> # noqa: E501
# python ./scripts/create_db_question.py -i 1 -p 3 -t "test question 3"


if __name__ == "__main__":
    import os
    import sys

    from dotenv import load_dotenv

    module_path = os.path.abspath(os.path.join("src"))
    if module_path not in sys.path:
        sys.path.append(module_path)
    load_dotenv(override=True)

    import argparse

    from common.citation_db import create_question, create_template_question_lockfile, get_conn

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--template-id", required=True, help="The template_id of the template")
    parser.add_argument("-p", "--prefix", required=True, help="The prefix for the question")
    parser.add_argument("-t", "--text", required=True, help="The text of the question")

    args = parser.parse_args()

    conn_str = os.environ["CITATION_DB_CONNECTION_STRING"]
    try:
        conn = get_conn(conn_str)
        cursor = conn.cursor()
        question = create_question(
            conn=conn,
            cursor=cursor,
            template_id=args.template_id,
            prefix=args.prefix,
            text=args.text,
        )
        print("Question created.")
        output_path = create_template_question_lockfile(
            cursor=cursor,
            template_id=args.template_id,
        )
        print(f"Updated template question lockfile at path {output_path}")
    finally:
        cursor.close()
        conn.close()
