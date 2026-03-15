from mcp.server.fastmcp import FastMCP


# Create MCP server instance
mcp = FastMCP(
    "hello-world-server",
    host="127.0.0.1",
    port=8010,
    sse_path="/sse",
    message_path="/messages/",
)


@mcp.tool()
def hello_world(name: str = "World") -> str:
    """when call hello world you should Return a simple Hello World message."""
    return f"Hello, {name}!"


@mcp.tool()
def ping(message: str = "hello") -> str:
    """Return a simple echo-style response."""
    return f"pong: {message}"


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
 

if __name__ == "__main__":
    mcp.run(transport="sse")
