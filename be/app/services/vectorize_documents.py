import os
from app.services.vectorstore import get_vectorstore
from app.util.get_file_chunks import get_file_chunks


def embedding_service_file(root_dir: str):
    if not os.path.exists(root_dir):
        print(f"Error: File not found: {root_dir}")
        return
    vectorstore = get_vectorstore()

    # define skip files and extensions
    skip_files = {'.DS_Store', '.gitignore', '.git', '__pycache__', '.pyc', '.pyo', '.pyd'}
    skip_extensions = {'.log', '.tmp', '.temp', '.swp', '.swo'}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for file_name in filenames:
            # skip system files and files that don't need to be processed
            if file_name in skip_files or file_name.startswith('.'):
                continue
            
            # check file extension
            file_ext = os.path.splitext(file_name)[1].lower()
            if file_ext in skip_extensions:
                continue
                
            file_path = os.path.join(dirpath, file_name)
            if not os.path.isfile(file_path):
                continue
                
            try:
                chunks = get_file_chunks(file_path)
                chunk_texts = [chunk.page_content for chunk in chunks]
                if not chunk_texts:
                    continue

                # calculate relative path and subdirectory
                rel_filepath = os.path.relpath(file_path, root_dir)     # relative path to root directory
                sub_dir = os.path.dirname(rel_filepath)                 # subdirectory, could be empty string

                # construct metadata
                metadatas = [
                    {
                        "root_dir": root_dir,
                        "sub_dir": sub_dir,            # subdirectory (e.g. 'sub1/sub2', empty string in root directory)
                        "file": file_name,             # file name
                        "filepath": file_path,         # absolute path
                        "rel_filepath": rel_filepath,  # relative path to root directory
                        "chunk_id": idx
                    }
                    for idx in range(len(chunk_texts))
                ]
                # batch insert into Qdrant
                vectorstore.add_texts(chunk_texts, metadatas=metadatas)
                print(f"Inserted {len(chunk_texts)} chunks for file: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue
