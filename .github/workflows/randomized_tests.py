name: Randomized tests
on:
  push:
    branches:
      - '*'
  schedule:
    - cron:  '42 3 * * *'
  workflow_dispatch:
jobs:
  randomized_tests:
    name: Randomized tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        name: Install Python
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -U -r requirements.txt -c constraints.txt
          pip install -U -r requirements-dev.txt coveralls -c constraints.txt
          pip install -c constraints.txt -e .
          pip install "qiskit-terra"
          pip install "qiskit-ibmq-provider" -c constraints.txt
          pip install "qiskit-aer"
      - name: Run randomized tests
        run: python3 -m unittest discover -s test/randomized -t . -v
      - name: Create comment on failed test run
        if: ${{ failure() }}
        uses: peter-evans/create-or-update-comment@v1
        with:
          issue-number: 16
          body: |
            Randomized tests failed at commit ${{ github.sha }}.
            _Logs_: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}.
