// File: src/App.tsx
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Alert,
  Spinner,
  Card,
} from "react-bootstrap";
import { BsFileEarmarkText, BsEnvelopePaper } from "react-icons/bs";
import "bootstrap/dist/css/bootstrap.min.css";

const gradientBg = {
  minHeight: "100vh",
  background: "linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%)",
  padding: "40px 0",
};

const App: React.FC = () => {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [cvFeedback, setCvFeedback] = useState<string | null>(null);
  const [coverLetter, setCoverLetter] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setCvFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setCvFeedback(null);
    setCoverLetter(null);

    if (!cvFile) {
      setError("Please upload a CV file.");
      return;
    }
    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("cv_file", cvFile);
    formData.append("job_desc", jobDescription);

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/uploadfile/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setCvFeedback(response.data.cv_review_task || response.data.cv_review || "No feedback found.");
      setCoverLetter(response.data.cover_letter_task || response.data.cover_letter || "No cover letter found.");
    } catch (err: any) {
      setError(err.response?.data?.detail || "An error occurred while submitting the form.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      ...gradientBg,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <Container style={{ maxWidth: 950 }}>
        <Card className="shadow-lg mb-5" style={{ borderRadius: 18 }}>
          <Card.Body>
            <Card.Title
              as="h1"
              className="mb-4 text-center"
              style={{
                fontWeight: 700,
                fontSize: "2.5rem",
                color: "#3b82f6",
                letterSpacing: 1,
              }}
            >
              CV & Cover Letter Generator
            </Card.Title>
            <Form onSubmit={handleSubmit}>
              <Form.Group controlId="formFile" className="mb-4">
                <Form.Label>
                  <strong>Upload your CV (PDF):</strong>
                </Form.Label>
                <Form.Control
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  style={{ borderRadius: 10, padding: 10 }}
                />
              </Form.Group>
              <Form.Group controlId="formJobDesc" className="mb-4">
                <Form.Label>
                  <strong>Job Description:</strong>
                </Form.Label>
                <Form.Control
                  as="textarea"
                  rows={8}
                  value={jobDescription}
                  onChange={e => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  style={{
                    fontSize: 16,
                    borderRadius: 10,
                    padding: 12,
                    background: "#f8fafc",
                  }}
                />
              </Form.Group>
              <div className="d-grid">
                <Button
                  variant="primary"
                  type="submit"
                  disabled={loading}
                  size="lg"
                  style={{
                    borderRadius: 10,
                    fontWeight: 600,
                    letterSpacing: 1,
                  }}
                >
                  {loading ? (
                    <>
                      <Spinner animation="border" size="sm" /> Submitting...
                    </>
                  ) : (
                    "Submit"
                  )}
                </Button>
              </div>
            </Form>
            {error && (
              <Alert variant="danger" className="mt-3" style={{ borderRadius: 10 }}>
                {error}
              </Alert>
            )}
          </Card.Body>
        </Card>

        {(cvFeedback || coverLetter) && (
          <Row>
            <Col md={6}>
              <Card className="mb-4 shadow" style={{ borderRadius: 16, background: "#f1f5f9" }}>
                <Card.Body>
                  <Card.Title className="d-flex align-items-center mb-3" style={{ color: "#0ea5e9" }}>
                    <BsFileEarmarkText size={28} className="me-2" />
                    CV Feedback
                  </Card.Title>
                  <Card.Text style={{ whiteSpace: "pre-wrap", fontSize: 16 }}>
                    {cvFeedback}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={6}>
              <Card className="mb-4 shadow" style={{ borderRadius: 16, background: "#f1f5f9" }}>
                <Card.Body>
                  <Card.Title className="d-flex align-items-center mb-3" style={{ color: "#16a34a" }}>
                    <BsEnvelopePaper size={26} className="me-2" />
                    Cover Letter
                  </Card.Title>
                  <Card.Text style={{ whiteSpace: "pre-wrap", fontSize: 16 }}>
                    {coverLetter}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
};

export default App;