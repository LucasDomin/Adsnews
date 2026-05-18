from fastapi import APIRouter
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from analyzers.creative_analyzer import analyze_creative_text

router = APIRouter()


def compute_score(a: dict) -> int:
    return int(
        min(a["urgency_score"] * 15, 30) +
        min(a["trust_score"] * 20, 30) +
        min(a["speed_score"] * 15, 20) +
        min(a["accessibility_score"] * 10, 20)
    )


def tier(score: int) -> str:
    return "Alto" if score >= 60 else "Médio" if score >= 30 else "Baixo"


def p_dev(a: dict, text: str) -> dict:
    risks, suggestions = [], []
    if len(text) > 300:
        risks.append("Copy longo — risco de truncamento em mobile")
    if a["trust_score"] == 0:
        risks.append("Zero sinais de credibilidade detectados")
        suggestions.append("Adicione: 'aprovado', 'oficial', 'seguro', 'garantia'")
    if a["urgency_score"] >= 3:
        suggestions.append("Urgência alta — teste versão mais suave para evitar fadiga")
    if not any(w in text.lower() for w in ["pix", "link", "acesse", "clique", "saiba"]):
        risks.append("Nenhum gatilho de ação técnica detectado")
    return {
        "label": "Desenvolvedor Sênior",
        "risks": risks or ["Sem riscos técnicos críticos"],
        "suggestions": suggestions or ["Estrutura técnica dentro do esperado"],
    }


def p_growth(a: dict, text: str) -> dict:
    risks, suggestions = [], []
    total = a["urgency_score"] + a["trust_score"] + a["speed_score"] + a["accessibility_score"]
    if total < 2:
        risks.append("Baixa densidade de sinais de conversão")
        suggestions.append("Adicione pelo menos 2 gatilhos: urgência ou confiança")
    if a["urgency_score"] >= 2 and a["trust_score"] >= 2:
        suggestions.append("Combinação urgência + confiança — alto potencial de CTR")
    if a["access_words"]:
        suggestions.append(f"Acessibilidade detectada: {', '.join(a['access_words'])} — bom para topo de funil")
    if a["urgency_score"] == 0:
        risks.append("Sem gatilhos de urgência — pode reduzir taxa de clique")
    return {
        "label": "Analista de Growth",
        "risks": risks or ["Potencial de crescimento razoável"],
        "suggestions": suggestions or ["Testar variações de CTA para otimizar CVR"],
    }


def p_data(a: dict, score: int) -> dict:
    breakdown = [
        f"Urgência: {a['urgency_score']} hits → {min(a['urgency_score']*15,30)}/30 pts",
        f"Confiança: {a['trust_score']} hits → {min(a['trust_score']*20,30)}/30 pts",
        f"Velocidade: {a['speed_score']} hits → {min(a['speed_score']*15,20)}/20 pts",
        f"Acessibilidade: {a['accessibility_score']} hits → {min(a['accessibility_score']*10,20)}/20 pts",
    ]
    return {
        "label": "Cientista de Dados",
        "tier": tier(score),
        "risks": [f"Score: {score}/100 — tier {tier(score)}"],
        "suggestions": breakdown,
    }


def p_creative(a: dict, text: str) -> dict:
    risks, suggestions = [], []
    has_u = a["urgency_score"] > 0
    has_t = a["trust_score"] > 0
    has_s = a["speed_score"] > 0
    if has_u and has_t and has_s:
        suggestions.append("Triângulo perfeito: urgência + confiança + velocidade presente")
    elif has_u and not has_t:
        risks.append("Urgência sem âncora de confiança — risco de rejeição")
        suggestions.append("Equilibre com sinal de autoridade ou garantia")
    elif has_t and not has_u:
        risks.append("Confiança sem urgência — CTR abaixo do potencial")
        suggestions.append("Adicione gatilho temporal: 'hoje', 'agora', 'por tempo limitado'")
    words = len(text.split())
    if words < 10:
        risks.append("Copy muito curto — pode não converter sem contexto")
    elif words > 50:
        risks.append("Copy longo demais para ad — considere versão condensada")
    return {
        "label": "Especialista Criativo",
        "risks": risks or ["Composição criativa equilibrada"],
        "suggestions": suggestions or ["Testar variação com headline mais emocional"],
    }


@router.post("/analyze")
def analyze_ad(payload: dict):
    parts = [payload.get("headline",""), payload.get("body",""), payload.get("cta","")]
    text = " ".join(p for p in parts if p).strip()
    if not text:
        return {"error": "Nenhum texto fornecido"}
    a = analyze_creative_text(text)
    score = compute_score(a)
    return {
        "score": score,
        "tier": tier(score),
        "raw_analysis": a,
        "perspectives": [
            p_dev(a, text),
            p_growth(a, text),
            p_data(a, score),
            p_creative(a, text),
        ],
    }