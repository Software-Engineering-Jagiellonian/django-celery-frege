import { Link } from "react-router-dom";

function Navbar() {
    return (
        <div>
            <nav
                style={{
                    borderBottom: "solid 1px",
                    paddingBottom: "1rem",
                }}
            >
                <Link to="/">Home</Link> |{" "}
                <Link to="/about">About</Link>
            </nav>
        </div>
    );
}

export default Navbar;