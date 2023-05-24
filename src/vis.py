import os
import signal
import streamlit as st

# from src.main import AuthorList
from main import AuthorList


def killing_button():
    st.sidebar.write("---")
    cond = st.sidebar.button("Stop program", key='boom')
    if cond:
        os.kill(int(os.environ['APP_PID']), signal.SIGTERM)
        os.kill(os.getpid(), signal.SIGTERM)


if 'APP_PID' in os.environ:
    killing_button()


authors = AuthorList()

authors.check_if_main_ready()
authors.check_if_ready_for_update()

if not authors.update_ready and not authors.main_ready:
    st.warning('Main file empty and no files to update it from. Copy paste files to "to_update" folder.')

if authors.main_ready:
    st.success('Main database is ready (not empty). You can prepare truncated lists for email sending')
    st.write(f'Number of all authors: {authors.main_file.shape[0]}')
    with st.expander("DB"):
        st.write(authors.main_file)

    authors_num = st.number_input('Number (n) of authors per file', 1, value=300)
    if st.button("Get file of n authors"):
        authors.create_db_of_n_authors(authors_num)
        authors.store_main_db()
        st._rerun()
    try:
        st.write(f'Number of all authors: {authors.not_sent.shape[0]}')
    except AttributeError:
        st.warning('Get file with n number of authors by pressing the button above')
else:
    st.warning('Main database is empty. If files for update are ready press the "Update main database" button first.')

if authors.update_ready:
    st.success('Files for updating database are ready.')
    if st.button("Update main database."):
        authors.main_file = authors.data_update()
        authors.store_main_db()
        st._rerun()
else:
    st.warning('No files to update main. Copy paste files to "to_update" folder.')
