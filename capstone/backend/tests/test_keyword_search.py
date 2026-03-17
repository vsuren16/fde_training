from app.services.keyword_search_service import KeywordSearchService


def test_keyword_search_returns_relevant_document() -> None:
    service = KeywordSearchService()
    service.load(
        [
            {
                "incident_id": "INC-1",
                "title": "VPN access denied for valid users",
                "description": "Remote vpn access denied for valid users",
                "resolution_notes": "Check VPN gateway and access policy.",
                "team": "Network Operations",
                "status": "Resolved",
                "incident_text": "VPN access denied for valid users. Network issue. Remote vpn access denied for valid users.",
                "priority": 2,
                "category": "Network",
            },
            {
                "incident_id": "INC-2",
                "title": "Printer toner issue",
                "description": "Printer toner issue at branch office",
                "resolution_notes": "Replace toner cartridge.",
                "team": "Field Support",
                "status": "Resolved",
                "incident_text": "Printer toner issue at branch office. Hardware issue.",
                "priority": 4,
                "category": "Hardware",
            },
        ]
    )

    results = service.search("users are denied remote vpn access", top_k=3)

    assert results
    assert results[0]["incident_id"] == "INC-1"
