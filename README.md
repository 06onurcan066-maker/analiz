# Dynamic Bet & Score Analytics Engine

Bu repo, "Dynamic Bet & Score Analytics Engine" projesinin başlangıç iskeletini içerir. Backend FastAPI tabanlıdır ve Poisson + Monte Carlo simülasyon motorunu barındırır. Frontend için Next.js + Tailwind önerilmektedir; frontend iskeleti ayrı bir branch veya klasör olarak eklenecektir.

Özellikler (ilk sürüm):
- Asenkron FastAPI servisleri
- API-Football entegrasyonu (httpx ile)
- Poisson lambdaları ve 10.000 Monte Carlo simülasyonu (run_in_executor ile)
- Value Bet ve SureBet hesaplama
- Docker Compose ile temel servisler: Postgres, Redis

Kurulum (lokal):
1) Repo klonla
   git clone https://github.com/06onurcan066-maker/analiz.git
2) .env dosyasını oluştur (örnek: .env.example)
3) Docker Compose ile çalıştır
   docker-compose up --build
4) Backend çalışır durumda olacaktır: http://localhost:8000

API endpointleri:
- GET /health
- POST /api/simulate  -> Simülasyon çalıştırma
- GET /api/external/fixtures -> API-Football'dan fixture çekme

Güvenlik notları:
- API anahtarlarını ve OAuth secret'larını asla public repo'ya commit etmeyin. GitHub Secrets, Docker secrets veya Kubernetes secrets kullanın.

Devam adımları (plan):
- Frontend Next.js + Tailwind + NextAuth Google giriş
- Celery görev kuyruğu ile asenkron simülasyon yönetimi
- WebSocket tabanlı canlı odds ingestion
- UI (Türkçe) ve görselleştirmeler

