"""Tests for the stdio transport boundary."""

from __future__ import annotations

from openlist_mcp import config, server


def test_startup_diagnostics_do_not_corrupt_stdio(monkeypatch, capsys) -> None:
    """Only the MCP run loop may write protocol data to stdout."""
    monkeypatch.setenv("OPENLIST_URL", "https://openlist.example.test")
    monkeypatch.setenv("OPENLIST_USERNAME", "user")
    monkeypatch.setenv("OPENLIST_PASSWORD", "test-password")
    monkeypatch.setenv("OPENLIST_SKILLS", "core")
    config._config = None

    def noisy_registration() -> None:
        print("registration diagnostic")

    def fake_run() -> None:
        print("mcp protocol")

    monkeypatch.setattr(server, "register_all_tools", noisy_registration)
    monkeypatch.setattr(server.mcp, "run", fake_run)

    server.main()
    captured = capsys.readouterr()

    assert captured.out == "mcp protocol\n"
    assert "registration diagnostic\n" in captured.err
