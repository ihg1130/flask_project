# 🕊️ 하늘거울 (CHUMO) — 온라인 추모 서비스

**하늘거울**은 Python과 Flask를 기반으로 개발한 온라인 추모 웹 프로젝트입니다. 고인을 기억하고 추모할 수 있는 온라인 공간을 제공하며, 추모 프로필과 추모글을 관리하고 사용자 간의 추억을 공유할 수 있도록 구현했습니다.

## 📌 프로젝트 소개

- **프로젝트명:** 하늘거울 (CHUMO)
- **프로젝트 유형:** 온라인 추모 및 장례 관련 웹 서비스
- **개발 언어:** Python
- **웹 프레임워크:** Flask
- **데이터베이스:** SQLAlchemy ORM 기반 데이터 관리
- **프로젝트 목적:** 온라인 추모 공간을 통한 고인에 대한 기억과 추억 공유

## ✨ 주요 기능

### 1. 회원 관리
- 회원가입 및 로그인
- 로그아웃 및 세션 관리
- 비밀번호 해시 처리
- 로그인 사용자 기반 기능 접근 제어

### 2. 온라인 추모 공간
- 고인 프로필 등록
- 고인의 이름, 출생일, 사망일 및 추모 내용 관리
- 프로필 이미지 등록 및 관리
- 추모 공간 및 갤러리 조회

### 3. 추모 게시판
- 추모글 작성 및 조회
- 게시글 수정 및 삭제
- 게시글 이미지 처리
- 게시글 추천 기능
- 페이지네이션을 통한 게시글 목록 조회

### 4. 댓글 기능
- 게시글 댓글 작성
- 댓글 수정 및 삭제
- 댓글 추천 기능

### 5. 추모 콘텐츠 관리
- 추모 갤러리
- 추모 타임라인
- 추모 관련 메시지 및 공간 관리 화면

### 6. 인증 및 데이터 관리
- Flask 세션 기반 사용자 인증
- Flask-SQLAlchemy를 통한 데이터베이스 연동
- Flask-Migrate를 통한 데이터베이스 마이그레이션
- 카카오 OAuth 인증 관련 코드

## 🛠️ 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Python, Flask |
| ORM | Flask-SQLAlchemy, SQLAlchemy |
| Database Migration | Flask-Migrate |
| Authentication | Flask Session, Werkzeug Security |
| Form Validation | Flask-WTF |
| Template Engine | Jinja2 |
| OAuth Integration | Kakao OAuth 관련 코드 |
| Database | SQLite 개발 설정 |
| Version Control | Git, GitHub |

## 📂 프로젝트 구조

```text
flask_project/
├── config/
│   ├── default.py
│   └── development.py
├── images/
├── migrations/
├── pybo/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── filter.py
│   └── views/
│       ├── main_views.py
│       ├── question_views.py
│       ├── answer_views.py
│       └── auth_views.py
├── CHUMO_ERD.png
├── pybo.db
└── README.md
```

## 🗃️ 데이터베이스 설계

데이터베이스는 Flask-SQLAlchemy ORM을 활용하여 구성했습니다.

주요 모델은 다음과 같습니다.

| 모델 | 역할 |
|---|---|
| User | 사용자 계정 정보 관리 |
| Chumo | 고인 프로필 및 추모 정보 관리 |
| Question | 추모 게시글 관리 |
| Answer | 게시글 댓글 관리 |

게시글과 댓글의 추천 관계는 별도의 연결 테이블을 통해 관리합니다.

데이터베이스 설계도: [CHUMO_ERD.png](./CHUMO_ERD.png)

## ⚙️ 개발 환경 설정

### 1. 저장소 클론

```bash
git clone https://github.com/ihg1130/flask_project.git
cd flask_project
```

### 2. 가상환경 생성

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 필요한 라이브러리 설치

프로젝트에서 사용하는 Flask 확장 라이브러리를 설치합니다.

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-WTF Flask-JWT-Extended Flask-Mail requests tinydb
```

프로젝트의 실제 의존성에 따라 추가 패키지가 필요할 수 있습니다.

### 4. 환경 변수 설정

애플리케이션은 `APP_CONFIG_FILE` 환경 변수를 통해 설정 파일을 불러옵니다.

Windows PowerShell:

```powershell
$env:APP_CONFIG_FILE = (Resolve-Path ".\config\development.py").Path
$env:FLASK_APP = "pybo"
$env:FLASK_DEBUG = "true"
```

macOS / Linux:

```bash
export APP_CONFIG_FILE="$(pwd)/config/development.py"
export FLASK_APP=pybo
export FLASK_DEBUG=true
```

### 5. 애플리케이션 실행

```bash
flask run
```

브라우저에서 아래 주소로 접속합니다.

http://127.0.0.1:5000

> 최초 실행 시 데이터베이스 마이그레이션 및 초기화가 필요할 수 있습니다. 개발 환경 설정과 기존 데이터베이스 상태를 확인한 후 실행하세요.

## 🖥️ 주요 페이지

| 경로 | 기능 |
|---|---|
| `/` | 메인 페이지 |
| `/memorial` | 추모 관련 페이지 |
| `/question/list/` | 추모 게시글 목록 |
| `/question/create/` | 추모 게시글 작성 |
| `/question/new` | 고인 프로필 등록 |
| `/auth/signup/` | 회원가입 |
| `/auth/login/` | 로그인 |
| `/auth/logout/` | 로그아웃 |

일부 기능은 로그인이 필요합니다.

## 🔒 보안 및 운영 시 고려 사항

- 운영 환경에서는 `SECRET_KEY`, JWT 서명 키 및 OAuth 비밀키를 환경 변수나 별도 비밀 관리 시스템으로 관리합니다.
- 저장소에 인증 비밀키가 노출된 경우 해당 키를 폐기하고 재발급합니다.
- 디버그 모드는 운영 환경에서 비활성화합니다.
- 개인정보 및 추모 콘텐츠를 안전하게 보관하기 위한 접근 제어와 백업 정책을 마련합니다.

## 🚀 향후 개선 방향

- 반응형 UI 및 모바일 사용성 개선
- 추모 공간별 접근 권한 및 공유 기능 강화
- 추모 콘텐츠 검색 기능 개선
- 이미지 저장 및 관리 구조 개선
- 운영 환경 배포 및 보안 설정 강화

## 📄 License

별도의 라이선스가 지정되지 않은 경우, 사용 및 재배포 조건을 검토한 후 라이선스를 추가해 주세요.
