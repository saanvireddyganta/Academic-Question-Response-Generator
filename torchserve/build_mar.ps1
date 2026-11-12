$M=(Resolve-Path "model\\distilgpt2").Path
$H=(Resolve-Path "torchserve\\handler.py").Path
New-Item -ItemType Directory -Force -Path "torchserve\\model_store" | Out-Null
torch-model-archiver --model-name academic_generator --version 1.0 --serialized-file "$M\\pytorch_model.bin" --handler "$H" --extra-files "$M\\config.json,$M\\generation_config.json,$M\\merges.txt,$M\\special_tokens_map.json,$M\\tokenizer_config.json,$M\\tokenizer.json,$M\\vocab.json" --export-path "torchserve\\model_store" --force
