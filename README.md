# Academic Question Response Generator

Project 1 from the NLP Unit 5 assignment. Uses DistilGPT2, PyTorch, Transformers, Streamlit, TorchServe and provides a SageMaker deployment guide.

## Windows setup (Python 3.10 recommended)
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\download_model.py
python scripts\smoke_test.py
streamlit run app\streamlit_app.py
```
If activation is blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## Testing
`python scripts\run_test_suite.py` creates `reports\test_results.csv` using actual generated outputs. Test empty and long questions too.

## TorchServe
TorchServe is in limited maintenance. Verify the pinned TorchServe/PyTorch/Transformers versions together.
```powershell
pip install -r torchserve\requirements-torchserve.txt
.\torchserve\build_mar.ps1
docker build -f torchserve\Dockerfile -t academic-generator .
docker run --rm -p 8080:8080 -p 8081:8081 -p 8082:8082 academic-generator
```
Test:
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/predictions/academic_generator -ContentType "application/json" -Body '{"prompt":"Explain CNN","max_new_tokens":60}'
```

## SageMaker
See `sagemaker/README.md`. Use only faculty-approved AWS credentials, region, role, instance type and compatible TorchServe inference image. SageMaker does not automatically use TorchServe in every deployment. Active endpoints can incur charges; delete endpoints and unused resources after demonstration.

## Checklist
- [x] DistilGPT2/PyTorch local inference code
- [x] Academic question input and short/medium response setting
- [x] TorchServe handler and configuration
- [x] Streamlit with local PyTorch, TorchServe and SageMaker modes
- [x] Ten-prompt test script and input validation
- [ ] Run locally and capture screenshots
- [ ] Build/test TorchServe container
- [ ] Deploy/invoke approved SageMaker endpoint
- [ ] Record actual latency/configuration and cloud cleanup
- [ ] Complete report and presentation

Model weights are downloaded on first run; they are not included in this ZIP.
