# Public Codex Task Kit

제한된 코딩 환경에서 사용하는 범용 Skill과 작은 작업 하네스입니다. 특정 과제의 코드·데이터·답안은 포함하지 않습니다. 공개 자료 활용이 허용된 경우에만 사용하고, 플랫폼·과제 지침을 우선합니다.

## 필요한 것만 포함

| 구성 | 역할 | 적용 시점 |
| --- | --- | --- |
| `task-brief` | 요구사항·필수 산출물·검증 기준을 짧게 정리 | 새 과제 시작·요구사항 변경 |
| `verification-before-completion` | 실제 검증 없이 완료했다고 말하지 않도록 확인 | 수정 완료·결과 보고 전 |
| `ui-ux-pro-max` | 로컬 데이터에서 UI·UX·접근성·반응형 지침 검색 | UI가 있는 과제에만 |
| `harness/AGENTS.md` | 읽기 → 최소 계획 → 구현 → 검증 → 근거 기록 | 코딩 작업의 공통 흐름 |

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
git clone --depth 1 --branch v1.0.0 https://github.com/losnah-think/public-codex-task-kit.git "$kit_dir"
kit_ref="$(git -C "$kit_dir" rev-parse HEAD)"

# --check는 변경 없이 충돌과 설치 경로만 확인
python3 "$kit_dir/scripts/install.py" --project "$task_project" --ref "$kit_ref" --check

# 위 검사가 성공한 경우에만 실제 설치
python3 "$kit_dir/scripts/install.py" --project "$task_project" --ref "$kit_ref"
)
```

위 명령은 순서대로 실행하고 오류가 나오면 중단하세요. 파일을 덮어쓰거나 우회해서 진행하지 않습니다. 정확한 재현이 필요하면 공개 릴리스의 전체 commit SHA를 확인하고 그 SHA를 checkout한 뒤 설치하세요. 설치 영수증의 `supplied_ref`는 호출자가 전달한 값이며, 스크립트가 GitHub에 조회해 진위를 보증하는 값은 아닙니다.

4. 사용 중인 Codex는 `/exit` 후 기존 프로젝트 루트에서 `codex`로 다시 시작합니다. `/status`로 허용 모델을 다시 확인하고 `/skills`에서 설치된 Skill이 보이는지 확인합니다. 새 `AGENTS.md` 지침은 새 세션에서 읽힙니다.
5. `$task-brief`로 실제 과제의 요구사항과 확인 방법을 정리하고 작업합니다. UI가 있는 경우에만 `$ui-ux-pro-max`를 사용합니다. 끝내기 전 `$verification-before-completion`으로 실제 확인 결과를 기록합니다.

Skill 발견 방식은 제공 환경 버전에 따라 다를 수 있습니다. 목록에 보이지 않으면 제공 Codex에게 설치된 `.agents/skills/` 파일을 읽게 하거나 플랫폼의 안내 수단에 문의하세요. 플랫폼 설정·관리 프로세스는 변경하지 않습니다.

## 설치기가 하는 일

- 프로젝트의 `.agents/skills/`에 Skill·필요 데이터·라이선스를 복사합니다.
- `.agents/public-task-kit/`에 하네스·출처·라이선스·파일 해시 영수증을 저장합니다.
- 기존 `AGENTS.md` 내용은 유지하고 짧은 추가 지침 링크만 붙입니다. 기존 프로젝트·플랫폼 지침은 계속 우선합니다.
- 같은 파일로 다시 실행하면 변경하지 않습니다. 다른 내용의 파일이 있으면 덮어쓰기 전에 중단합니다.
- 네트워크·외부 명령·패키지 설치·전역 설정·API 키·모델·Git remote를 변경하지 않습니다. Python 3.9 이상 표준 라이브러리만 필요합니다. Python 3.9.6에서 검증했습니다.

상위 지침이나 `AGENTS.override.md`가 있는 경우 그 지침이 우선합니다. 설치된 하네스가 자동으로 적용되지 않으면 제공 Codex에서 파일을 명시적으로 읽어 확인하세요.

## UI UX Pro Max 사용

UI가 없는 과제에는 실행할 필요가 없습니다. 실제 스택을 확인한 뒤 관련 검색만 실행하세요. 검색은 번들 CSV와 Python 코드로 로컬에서 처리합니다.

```sh
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "dashboard readable accessible" --design-system
python3 .agents/skills/ui-ux-pro-max/scripts/search.py "keyboard focus" --domain ux
```

기존 UI 방향이나 디자인 시스템이 있으면 우선합니다. 검색 결과가 외부 글꼴·이미지 URL을 제안해도 자동으로 외부 자원을 연결하지 마세요. 플랫폼 허용 범위와 네트워크 제약을 확인하고 로컬·시스템 자원을 우선합니다. UI 조작·촬영·브라우저 자동화는 이 키트에 포함되지 않습니다.

## 사용 기록과 유지

필수 계획·협업 문서가 지정돼 있으면 그 문서에 실제 판단과 테스트 결과를 남깁니다. 별도 기록 양식이 필요할 때만 [빈 작업 기록](templates/WORKLOG.md)을 참고하세요. 설치기가 과제 산출물이나 답안을 생성하지는 않습니다.

출처·라이선스·사용 범위는 [SOURCES.md](SOURCES.md)에 있습니다. 원본 저장소와 이 키트의 공개 상태를 사용 전·제출 전에 확인하고, 요구된 결과 통지 전까지 이 저장소를 공개 상태로 유지하세요. 검토 기록은 제공 작업 환경에 남기며 **Git Push·외부 전송으로 기록하지 않습니다.**

이 키트는 운영 규정 준수를 자동으로 인증하지 않습니다. **Computer Use 금지와 AI 사용이 금지된 후속 단계의 제한도 그대로 적용**됩니다. 차단되면 설정을 우회하지 말고 플랫폼의 문제 신고를 이용하세요.

## 키트 개발 검증

```sh
python3 -m unittest discover -s tests -v
```

라이선스는 MIT이며, 외부에서 가져온 파일에는 해당 저작권과 라이선스를 보존합니다.
