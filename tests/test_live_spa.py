"""Guards the /live SPA against its nginx proxy whitelist: every upstream path the page calls must be allowed,
nothing sensitive may be, and the nginx regexes must stay quoted (unquoted {32} breaks nginx)."""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import dev_live  # noqa: E402

HTML = (ROOT / "live" / "index.html").read_text()
CONF = (ROOT / "default.conf").read_text()


def nginx_patterns():
    return re.findall(r'location ~ "\^/ah/\(\?<up>(.*?)\)\$"', CONF)


def test_every_spa_call_is_whitelisted():
    calls = set(re.findall(r'api\(\s*[`"]([^`"?]+)[`"]', HTML)) | set(re.findall(r'api\(\s*`([^`]+)`', HTML))
    assert calls
    pats = [re.compile("^(?:" + p + ")$") for p in nginx_patterns()]
    for c in calls:
        c = re.sub(r"\$\{[^}]*\}", "sec_" + "0" * 32 if "historic" in c else "prf_" + "0" * 32, c)
        c = c.replace("encodeURIComponent(S)", "NVDA")
        if c.endswith("/"):
            c += "2026-10-16" if "hours" in c else "NVDA"
        assert any(p.match(c) for p in pats), f"not whitelisted in nginx: {c}"
        assert dev_live.ALLOW.match(c), f"not whitelisted in dev proxy: {c}"


def test_whitelist_blocks_sensitive_routes():
    pats = [re.compile("^(?:" + p + ")$") for p in nginx_patterns()]
    for bad in ["_ah/admin/users/x/ban", "mjolnir/ban", "profile-settings", "orders/sync", "stonks/search", "search",
                "currency/balances/x", "stonks/security/sec_" + "0" * 32 + "/owners", "token/jwt"]:
        assert not any(p.match(bad) for p in pats), bad
        assert not dev_live.ALLOW.match(bad), bad


def test_nginx_strips_credentials_and_quotes_regexes():
    assert CONF.count('proxy_set_header Authorization "";') == len(nginx_patterns())
    assert CONF.count('proxy_set_header ah-user-id "";') == len(nginx_patterns())
    assert "location ~ ^/ah/" not in CONF  # unquoted regex with {32} would break nginx
    assert "proxy_cache_path" in CONF


def test_spa_escapes_user_content():
    assert "esc(p.title" in HTML and "safeUrl(" in HTML
