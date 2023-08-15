import os
import time
import threading

import firebase_admin

from firebase_admin import credentials, firestore

from authorizations import create_json

CURRENT_FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(CURRENT_FILE_LOCATION, "creds.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()


def process_document_change(doc_snapshot):
    document_data = doc_snapshot.to_dict()
    status = document_data.get("status")

    if status == "not_done" and document_data.get("count", 0) > 0:
        doc_snapshot.reference.update({"status": "in_work"})
        worker_doc_ref = db.collection("workers").document("count")
        worker_data = worker_doc_ref.get().to_dict()
        worker_count = worker_data.get("count", 0)
        worker_count += 1
        worker_doc_ref.update({"count": worker_count})

        constraints = document_data.get("constraints", [])
        result_ids = document_data.get("result", [])
        count = document_data.get("count")

        if count > 0:
            current_index = len(result_ids) - count

            if current_index >= 0:
                result_id = result_ids[current_index]
                count -= 1

                thread = threading.Thread(
                    target=create_json,
                    args=(result_id, constraints, worker_count),
                )
                thread.start()

                print(f"Processing... Remaining count: {count}")

        worker_doc_ref.update({"count": worker_count - 1})
        if count == 0:
            doc_snapshot.reference.update({"status": "done"})
            print("Processing completed.")
        else:
            doc_snapshot.reference.update({"count": count, "status": "not_done"})


def firestore_listener():
    collection_ref = db.collection("tasks")

    def on_snapshot(doc_snapshot, changes, read_time):
        for change in changes:
            # Process only modified or created documents
            if change.type.name == "MODIFIED" or change.type.name == "ADDED":
                process_document_change(change.document)

    doc_watch = collection_ref.on_snapshot(on_snapshot)


if __name__ == "__main__":
    firestore_listener()
    try:
        while True:
            time.sleep(10)  # main thread will sleep for 10 seconds at a time
    except KeyboardInterrupt:
        print("Stopping listener...")
