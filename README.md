# Public Codex Task Kit

제한된 코딩 환경에서 사용하는 범용 Skill과 작은 작업 하네스입니다. 특정 과제의 코드·데이터·답안은 포함하지 않습니다. 공개 자료 활용이 허용된 경우에만 사용하고, 플랫폼·과제 지침을 우선합니다.

## 짧게 시작하기

제공 Codex에 아래 한 줄을 입력하면 [최종 프롬프트](START.md)를 읽고 설치부터 현재 세션의 Skill 적용까지 진행할 수 있습니다.

```text
https://raw.githubusercontent.com/losnah-think/public-codex-task-kit/v1.1.1/START.md 읽고 실행해줘.
```

터미널에서 설치만 진행하려면 실제 과제 프로젝트 루트에서 실행하세요. 전체 파일을 받은 뒤 실행하므로 다운로드가 실패하면 설치를 시작하지 않습니다.

```sh
python3 -c 'import urllib.request; exec(urllib.request.urlopen("https://raw.githubusercontent.com/losnah-think/public-codex-task-kit/v1.1.1/setup.py", timeout=20).read())'
```

설치 도우미는 **v1.1.1**, 설치되는 Skill·하네스는 기존의 검증된 **v1.1.0 / 8e7435af2fe28cc57cfffde178822987b8e3fb46**으로 고정돼 있습니다. 설치 뒤 현재 Codex에 지침을 적용하는 절차는 START.md에 있습니다. 터미널 설치기가 실행 중인 Codex의 지침을 자동 변경했다고 주장하지는 않습니다.

## 필요한 것만 포함

| 구성 | 역할 | 적용 시점 |
| --- | --- | --- |
| `task-brief` · `verification-before-completion` | 요구사항·산출물·검증 기준과 실제 결과 확인 | 시작·마무리 |
| `ui-ux-pro-max` · `antislop` · `antislop-copywriting` | 로컬 UI/UX 검색과 디자인·문구의 과장·반복 점검 | UI·사람이 읽는 문구 작성 |
| `humanize-korean` · `proofread` | 뜻을 보존한 한국어 윤문, 맞춤법·띄어쓰기·비문 교정 | 한국어 문구·문서 작성 |
| `harness/AGENTS.md` · 설치기 | 읽기 → 최소 계획 → 구현 → 검증 → 근거 기록 | 공통 흐름·안전한 설치/갱신 |

코딩 모델이나 MCP 서버를 추가하지 않습니다. 전체 Superpowers 플러그인, 브라우저 자동화, 외부 모델 호출, 원격 저장·원격 제어는 포함하지 않습니다.

## 설치 순서

모든 명령은 **제공된 작업 환경 안에서**, 공개 자료를 가져오는 허용된 경로로 실행합니다. 개인 PC 파일 업로드나 로컬 결과 반입용으로 사용하지 않습니다. 설치 전 코드와 [출처](SOURCES.md)를 확인하세요.

1. 과제 README와 운영 규정에서 공개 Skill 사용 가능 여부와 필수 파일명을 확인합니다.
2. 제공 Codex에서 `/status`와 `/model`로 허용된 모델·권한을 확인합니다. 개인 키·구독·모델 설정을 추가하지 않습니다.
3. 아래 명령을 프로젝트 루트에서 실행합니다. 키트는 임시 폴더에 받고 **기존 프로젝트 폴더를 작업 대상으로 유지**합니다.

```sh
# 제공 환경의 실제 프로젝트 루트에서 실행
(
set -eu
task_project="$PWD"
kit_dir="$(mktemp -d)"
git clone --depth 1 --branch v1.1.0 https://github.com/losnah-think/public-codex-task-kit.git "$kit_dir"
kit_ref="$(git -C "$kit_dir" rev-parse HEAD)"

# 이전 영수증이 있으면 검증된 관리 파일만 갱신
set --
if [ -f "$task_project/.agents/public-task-kit/source.json" ]; then
  set -- --upgrade
fi

# --check는 변경 없이 충돌과 설치 경로만 확인
python3 "$kit_dir/scripts/install.py" --project "$task_project" --ref "$kit_ref" --check "$@"

# 위 검사가 성공한 경우에만 실제 설치
python3 "$kit_dir/scripts/install.py" --project "$task_project" --ref "$kit_ref" "$@"
)
```

위 명령은 순서대로 실행하고 오류가 나오면 중단하세요. 파일을 덮어쓰거나 우회해서 진행하지 않습니다. 정확한 재현이 필요하면 공개 릴리스의 전체 commit SHA를 확인하고 그 SHA를 checkout한 뒤 설치하세요. 설치 영수증의 `supplied_ref`는 호출자가 전달한 값이며, 스크립트가 GitHub에 조회해 진위를 보증하는 값은 아닙니다.

4. 사용 중인 Codex는 `/exit` 후 기존 프로젝트 루트에서 `codex`로 다시 시작합니다. `/status`로 허용 모델을 다시 확인하고 `/skills`에서 설치된 Skill이 보이는지 확인합니다. 새 `AGENTS.md` 지침은 새 세션에서 읽힙니다.
5. `$task-brief`로 실제 과제의 요구사항과 확인 방법을 정리하고 작업합니다. UI가 있는 경우 `$ui-ux-pro-max`와 `$antislop`을 적용합니다. 사람이 읽는 문구에는 `$antislop-copywriting`, 한국어 윤문에는 `$humanize-korean`, 맞춤법·띄어쓰기·비문에는 `$proofread`를 사용합니다. 끝내기 전 `$verification-before-completion`으로 실제 확인 결과를 기록합니다.

Skill 발견 방식은 제공 환경 버전에 따라 다를 수 있습니다. 목록에 보이지 않으면 제공 Codex에게 설치된 `.agents/skills/` 파일을 읽게 하거나 플랫폼의 안내 수단에 문의하세요. 플랫폼 설정·관리 프로세스는 변경하지 않습니다.

## 로컬 설치기 scripts/install.py가 하는 일

- 프로젝트의 `.agents/skills/`에 Skill·필요 데이터·라이선스를 복사합니다.
- `.agents/public-task-kit/`에 하네스·출처·라이선스·파일 해시 영수증을 저장합니다.
- 기존 `AGENTS.md` 내용은 유지하고 짧은 추가 지침 링크만 붙입니다. 기존 프로젝트·플랫폼 지침은 계속 우선합니다.
- 같은 파일로 다시 실행하면 변경하지 않습니다. 다른 내용의 파일이 있으면 덮어쓰기 전에 중단합니다.
- `--upgrade`는 이전 영수증의 저장소·경로·해시를 확인하고, 기록된 그대로인 관리 파일만 갱신합니다. 사용자가 수정·삭제한 파일이나 새 파일과의 충돌이 있으면 쓰기 전에 중단합니다. 삭제 기능은 없습니다. 교체는 파일 단위로 수행되므로 디스크 오류 등으로 중단되면 성공으로 간주하지 말고 상태를 확인하세요.
- 네트워크·외부 명령·패키지 설치·전역 설정·API 키·모델·Git remote를 변경하지 않습니다. Python 3.9 이상 표준 라이브러리만 필요합니다. Python 3.9.6에서 검증했습니다.

루트 `setup.py`는 위 로컬 설치기를 호출하는 다운로드 도우미입니다. 공개 저장소의 고정 버전만 임시 폴더로 Clone하고 SHA를 확인한 뒤, 사전 검사와 설치를 차례로 실행합니다. 작업 프로젝트의 기존 Git remote나 전역 설정은 변경하지 않습니다. 실패 시 우회 경로를 시도하지 않고 중단합니다.

상위 지침이나 `AGENTS.override.md`가 있는 경우 그 지침이 우선합니다. 설치된 하네스가 자동으로 적용되지 않으면 제공 Codex에서 파일을 명시적으로 읽어 확인하세요.

## UI UX Pro Max 사용

UI가 없는 과제에는 실행할 필요가 없습니다. 실제 스택을 확인한 뒤 관련 검색만 실행하세요. 검색은 번들 CSV와 Python 코드로 로컬에서 처리합니다.

```sh
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "dashboard readable accessible" --design-system
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "keyboard focus" --domain ux
```

기존 UI 방향이나 디자인 시스템이 있으면 우선합니다. 검색 결과가 외부 글꼴·이미지 URL을 제안해도 자동으로 외부 자원을 연결하지 마세요. 플랫폼 허용 범위와 네트워크 제약을 확인하고 로컬·시스템 자원을 우선합니다. UI 조작·촬영·브라우저 자동화는 이 키트에 포함되지 않습니다.

## 안티슬롭·한국어 윤문 사용

하네스는 UI와 문구를 만드는 동안 `antislop`을 **during(project default)** 모드로 적용합니다. 전역 설정을 읽거나 바꾸지 않습니다. 문구에는 `antislop-copywriting`을 함께 적용하고, 화면과 무관한 문서에는 UI 검사를 N/A로 표시합니다. 사람이 직접 확인하지 않은 화면·버튼 동작은 수동 확인 대기로 남깁니다.

```text
$antislop UI와 문구의 과장·반복·근거 없는 주장부터 점검하고 작업 중 적용해줘.
$humanize-korean 지정 문서의 번역투와 반복을 다듬되 사실·수치·날짜·이름·조건·인용은 보존해줘.
$proofread 윤문한 문서의 맞춤법·띄어쓰기·명백한 비문만 교정해줘.
```

한국어 윤문은 원문을 보존한 뒤 수행합니다. 사실·수치·조건·서법은 별도로 대조하고, 아래 로컬 스크립트로 변경률을 실제 계산합니다. **30% 이상은 경고, 50% 이상은 채택 금지·롤백, 종료 코드 3은 검증 오류**입니다. 숫자를 맞추려고 멀쩡한 문장을 바꾸지 않습니다.

```sh
python3 .agents/skills/humanize-korean/scripts/verify_change_rate.py --before ORIGINAL.txt --after EDITED.md
```

변경률은 수정 범위이며 사실 보존이나 문장 품질의 보증이 아닙니다. 코드·경로·식별자·정해진 숫자는 윤문 대상이 아닙니다. 이 기능도 제공 Codex 안에서만 쓰며, **AI가 금지된 후속 서술형에는 사용하지 않습니다.**

## 사용 기록과 유지

필수 계획·협업 문서가 지정돼 있으면 그 문서에 실제 판단과 테스트 결과를 남깁니다. 별도 기록 양식이 필요할 때만 [빈 작업 기록](templates/WORKLOG.md)을 참고하세요. 설치기가 과제 산출물이나 답안을 생성하지는 않습니다.

출처·라이선스·사용 범위는 [SOURCES.md](SOURCES.md)에 있습니다. 원본 저장소와 이 키트의 공개 상태를 사용 전·제출 전에 확인하고, 요구된 결과 통지 전까지 이 저장소를 공개 상태로 유지하세요. 검토 기록은 제공 작업 환경에 남기며 **Git Push·외부 전송으로 기록하지 않습니다.**

이 키트는 운영 규정 준수를 자동으로 인증하지 않습니다. **Computer Use 금지와 AI 사용이 금지된 후속 단계의 제한도 그대로 적용**됩니다. 차단되면 설정을 우회하지 말고 플랫폼의 문제 신고를 이용하세요.

## 키트 개발 검증

```sh
python3 -m unittest discover -s tests -v
```

라이선스는 MIT이며, 외부에서 가져온 파일에는 해당 저작권과 라이선스를 보존합니다.
