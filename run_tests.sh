#!/bin/bash
# Run pytest with Allure reporting and open the report

echo "🧪 Running pytest with Allure reporting..."
./env/bin/pytest app/tests -v

echo ""
echo "📊 Generating Allure report..."
allure generate allure-results -o allure-report --clean

echo ""
echo "🌐 Opening Allure report in browser..."
allure open allure-report
