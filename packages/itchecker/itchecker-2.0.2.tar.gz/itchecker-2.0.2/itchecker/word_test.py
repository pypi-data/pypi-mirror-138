if __name__ == '__main__':
    import win32com.client as win32
    import os

    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = True
    doc_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'author.docx')
    doc = word.Documents.Open(doc_path)
    doc
    fields_by_tag = {control.Tag: control for control in doc.Bookmarks}
    for control in doc.ContentControls:
        if control.Tag == 'field1':
            control.Range.Text = '15'
    doc.Fields.Update()
    print(fields_by_tag['field2'].Range.Text)
