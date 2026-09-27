# مراجعة العقود التجارية

مشروع Python أولي لمراجعة العقود. إعداد الحزم وتعريف متطلبات المشروع موجودان في `pyproject.toml`، ومصدر الحزمة داخل `src/application_contract_erview`.

> اتبع الخطوات في طرفية **WSL / Ubuntu**. بيئة `.venv` التي قد تكون موجودة على Windows منفصلة عن بيئة WSL ولا تستخدمها هذه الخطوات.

## المتطلبات

- Windows مع WSL2 وتوزيعة Ubuntu.
- اتصال بالإنترنت.
- مساحة كافية لتنزيل Miniconda واعتماديات Python.

المشروع يتطلب **Python 3.14 أو أحدث**، حسب `pyproject.toml` وملف `.python-version`.

## 1. افتح المشروع في WSL

افتح طرفية Ubuntu/WSL ثم انتقل إلى مجلد المشروع:

```bash
cd /mnt/d/APPLICATION_CONTRACT_REVIEW
```

إذا لم يكن هذا هو مسار المشروع عندك، استبدله بالمسار الصحيح داخل WSL. قرص `D:` يظهر عادة تحت `/mnt/d`.

## 2. ثبّت Miniconda داخل WSL

نفّذ هذه الأوامر في طرفية WSL، وليس PowerShell. الأوامر تنزّل ملف التثبيت إلى مجلد المنزل، ثم تشغّله وتحذفه بعد اكتمال التثبيت:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda.sh
~/miniconda3/bin/conda init bash
```

أغلق طرفية WSL وافتحها من جديد، أو حمّل إعداد Bash في الطرفية الحالية:

```bash
source ~/.bashrc
```

تأكد أن Conda أصبح متاحًا:

```bash
conda --version
```

إذا ظهرت `conda: command not found`، شغّل `~/miniconda3/bin/conda init bash` ثم أغلق الطرفية وافتحها من جديد.

## 3. أنشئ بيئة المشروع

من مجلد المشروع، أنشئ بيئة باسم `review_contract` مع Python 3.14 و`uv`:

```bash
conda create -n review_contract -c conda-forge python=3.14 pip uv -y
conda activate review_contract
```

تحقق أن الطرفية تستخدم Python الموجود في بيئة Conda:

```bash
python --version
which python
uv --version
```

يجب أن يعرض `python --version` الإصدار 3.14 أو أحدث، وأن يشير مسار `which python` إلى بيئة `review_contract` تحت `~/miniconda3/envs/`.

## 4. ثبّت المشروع واعتمادياته

والبيئة `review_contract` مفعّلة، نفّذ من جذر المشروع:

```bash
uv pip install -e .
```

هذا يثبّت المشروع في وضع التطوير، ويقرأ الاعتماديات من `pyproject.toml`. لا تحتاج إلى تثبيت `requirements.txt` بالإضافة إليه؛ الملف الحالي لا يتضمن كل الاعتماديات المعرّفة للمشروع.

تحقق من التثبيت:

```bash
python -m pip list
```

## 5. شغّل نقطة الدخول الحالية

المشروع حاليًا في مرحلة أولية؛ أمر التشغيل المعرّف في `pyproject.toml` يطبع رسالة تحقق بسيطة:

```bash
application-contract-erview
```

المتوقع أن ترى:

```text
Hello from application-contract-erview!
```

## 6. افتح المشروع في VS Code باستخدام WSL

من طرفية WSL داخل مجلد المشروع شغّل:

```bash
code .
```

في VS Code، اختر مفسّر Python الخاص ببيئة Conda `review_contract`. مساره المعتاد:

```text
/home/<اسم-مستخدم-WSL>/miniconda3/envs/review_contract/bin/python
```

يمكنك معرفة المسار الدقيق بعد تفعيل البيئة عبر:

```bash
which python
```

تأكد أن نافذة VS Code متصلة بـWSL؛ مفسّر Windows الموجود في `.venv` ليس هو مفسّر WSL.

## استخدام المشروع لاحقًا

كل مرة تفتح فيها طرفية WSL جديدة:

```bash
cd /mnt/d/APPLICATION_CONTRACT_REVIEW
conda activate review_contract
```

للخروج من البيئة:

```bash
deactivate
```

## مشاكل شائعة

- **`conda: command not found`:** نفّذ `~/miniconda3/bin/conda init bash`، ثم أعد فتح طرفية WSL.
- **`pip: command not found` أو تثبيت الحزم يذكر `externally-managed-environment`:** تأكد أنك فعّلت `review_contract` وأن `which python` يشير إلى `~/miniconda3/envs/review_contract/`. لا تثبّت `python3-pip` عبر `apt` لهذا المشروع ولا تستخدم `--break-system-packages`.
- **`uv: command not found`:** فعّل البيئة الصحيحة. إن لم يكن `uv` مثبتًا فيها، نفّذ `conda install -n review_contract -c conda-forge uv`.
- **لا تظهر الحزم في VS Code:** اختر مفسّر Conda داخل جلسة WSL، وليس مفسّر Windows أو `.venv` الخاصة به.
