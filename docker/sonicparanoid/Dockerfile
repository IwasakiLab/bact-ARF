FROM python:3.8
RUN pip3 install -U pip setuptools wheel cython scipy numpy pandas biopython mypy psutil scikit-learn filetype && \
    pip3 install --no-cache-dir sonicparanoid==1.3.5 && \
    sonicparanoid-get-test-data -o . && \
    sonicparanoid -i sonicparanoid_test/test_input -o sonicparanoid_test/test_output -p my_first_run -t 4 && \
    rm -rf sonicparanoid_test
CMD sonicparanoid

