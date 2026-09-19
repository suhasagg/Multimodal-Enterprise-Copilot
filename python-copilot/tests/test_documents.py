from app.documents import chunks,extract
def test_chunks_overlap():
    x=chunks("a "*2000,size=100,overlap=10)
    assert len(x)>1
def test_text_extract():
    assert extract(b"hello","text/plain")=="hello"
