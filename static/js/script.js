// API base URL
const API_BASE = '';

// Initialize EmailJS with your Public Key (wait for EmailJS to load)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize EmailJS when page loads
    if (typeof emailjs !== 'undefined') {
        emailjs.init("LW8AvJdD_7yUt0D9M");
        console.log("✅ EmailJS initialized");
    } else {
        console.error("❌ EmailJS library not loaded");
    }
    
    loadQuickRunningEvents();
    loadEventOptions();
    
    // Check if event was pre-selected from events page
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('event');
    if (eventId) {
        // Wait a bit for the dropdown to populate
        setTimeout(() => {
            const eventSelect = document.getElementById('event');
            eventSelect.value = eventId;
            eventSelect.scrollIntoView({ behavior: 'smooth', block: 'center' });
            eventSelect.focus();
        }, 500);
    }
});

// Load running events in compact format for homepage
async function loadQuickRunningEvents() {
    try {
        const response = await fetch(`${API_BASE}/api/events/`);
        const events = await response.json();
        
        const eventsContainer = document.getElementById('runningEventsQuick');
        
        // Filter only running events
        const now = new Date();
        const runningEvents = events.filter(event => {
            const startDate = new Date(event.start_date);
            const endDate = new Date(event.end_date);
            return event.status === 'ongoing' && startDate <= now && endDate >= now;
        });
        
        if (runningEvents.length === 0) {
            eventsContainer.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 2rem; background: #f9fafb; border-radius: 12px;">
                    <i class="fas fa-calendar-times" style="font-size: 2rem; color: #9ca3af; margin-bottom: 1rem;"></i>
                    <p style="color: #6b7280; margin: 0;">No events currently running</p>
                    <a href="/events/" style="color: var(--primary-color); text-decoration: none; font-weight: 500; display: inline-block; margin-top: 0.5rem;">
                        <i class="fas fa-arrow-right"></i> Check upcoming events
                    </a>
                </div>
            `;
            return;
        }
        
        // Show max 3 running events on homepage
        const displayEvents = runningEvents.slice(0, 3);
        
        let html = displayEvents.map(event => createQuickEventCard(event)).join('');
        
        if (runningEvents.length > 3) {
            html += `
                <div style="grid-column: 1/-1; text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
                    <p style="margin: 0 0 1rem 0; font-size: 1.1rem; font-weight: 600;">
                        <i class="fas fa-plus-circle"></i> ${runningEvents.length - 3} more events running
                    </p>
                    <a href="/events/" class="view-all-link" style="color: white; text-decoration: none; font-weight: 600; padding: 0.75rem 1.5rem; background: rgba(255,255,255,0.2); border-radius: 8px; display: inline-block; transition: all 0.3s;">
                        <i class="fas fa-list"></i> View All Events
                    </a>
                </div>
            `;
        }
        
        eventsContainer.innerHTML = html;
        
        // Add click handlers to quick register buttons
        document.querySelectorAll('.quick-register-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const eventId = e.target.dataset.eventId;
                const eventSelect = document.getElementById('event');
                eventSelect.value = eventId;
                eventSelect.scrollIntoView({ behavior: 'smooth', block: 'center' });
                eventSelect.focus();
            });
        });
        
    } catch (error) {
        console.error('Error loading events:', error);
        document.getElementById('runningEventsQuick').innerHTML = '<p style="text-align: center; color: #dc3545;">Error loading events</p>';
    }
}

// Create compact event card for homepage
function createQuickEventCard(event) {
    const availableSeats = event.max_capacity - event.registered_count;
    const capacityPercentage = (event.registered_count / event.max_capacity * 100).toFixed(0);
    
    return `
        <div class="event-card-quick">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                <h3 style="margin: 0; font-size: 1.2rem; color: #1f2937;">
                    <i class="fas fa-calendar-alt" style="color: var(--primary-color);"></i> ${event.name}
                </h3>
                <span class="event-status-badge live" style="font-size: 0.75rem;">
                    <i class="fas fa-circle"></i> LIVE
                </span>
            </div>
            
            <p style="margin: 0.5rem 0; color: #6b7280; font-size: 0.9rem;">
                <i class="fas fa-map-marker-alt" style="color: var(--primary-color); width: 16px;"></i> ${event.venue}
            </p>
            
            <div style="margin: 0.75rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; font-size: 0.85rem;">
                    <span style="color: #6b7280;"><i class="fas fa-users"></i> ${event.registered_count}/${event.max_capacity}</span>
                    <span style="color: ${availableSeats > 10 ? '#10b981' : availableSeats > 0 ? '#f59e0b' : '#ef4444'}; font-weight: 600;">
                        ${availableSeats} seats left
                    </span>
                </div>
                <div class="capacity-bar" style="height: 6px;">
                    <div class="capacity-fill" style="width: ${capacityPercentage}%; height: 6px;"></div>
                </div>
            </div>
            
            <button class="quick-register-btn" data-event-id="${event.id}">
                <i class="fas fa-ticket-alt"></i> Register Now
            </button>
        </div>
    `;
}

// Load events for dropdown
async function loadEventOptions() {
    try {
        const response = await fetch(`${API_BASE}/api/events/`);
        const events = await response.json();
        
        const eventSelect = document.getElementById('event');
        eventSelect.innerHTML = '<option value="">Choose an event...</option>' +
            events.map(event => `
                <option value="${event.id}">${event.name} - ${new Date(event.start_date).toLocaleDateString()}</option>
            `).join('');
    } catch (error) {
        console.error('Error loading event options:', error);
    }
}

// Select event from running events section
function selectEvent(eventId) {
    document.getElementById('event').value = eventId;
    document.getElementById('gatePassForm').scrollIntoView({ behavior: 'smooth' });
}

// Handle form submission
document.getElementById("gatePassForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const eventId = document.getElementById("event").value;
    const name = document.getElementById("name").value;
    const studentId = document.getElementById("id").value;
    const email = document.getElementById("email").value;

    if (!eventId) {
        alert("Please select an event");
        return;
    }

    try {
        // Create registration via API
        const response = await fetch(`${API_BASE}/api/registrations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                event: eventId,
                name: name,
                student_id: studentId,
                email: email
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Send email using EmailJS (your working frontend method)
            let emailSentViaEmailJS = false;
            const qrContainer = document.getElementById("qrcode");
            
            // Show loading state
            qrContainer.innerHTML = `
                <div class="qr-success">
                    <i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: var(--primary-color);"></i>
                    <p style="margin-top: 1rem;">Sending confirmation email...</p>
                </div>
            `;
            
            try {
                // Get event details for email
                const eventResponse = await fetch(`${API_BASE}/api/events/${eventId}/`);
                const eventData = await eventResponse.json();
                
                // Send via EmailJS
                await emailjs.send("service_4noajtf", "template_eh5mdow", {
                    name: name,
                    id: studentId,
                    email: email,
                    qr_code: data.qr_code_image,
                    event_name: eventData.name || 'Event',
                    event_venue: eventData.venue || 'TBA',
                    event_date: new Date(eventData.start_date).toLocaleString() || 'TBA'
                });
                emailSentViaEmailJS = true;
                console.log("✅ Email sent successfully via EmailJS to:", email);
            } catch (emailError) {
                console.error("❌ EmailJS failed:", emailError);
                emailSentViaEmailJS = false;
            }
            
            // Display QR code with email status
            const emailStatus = emailSentViaEmailJS
                ? '<p style="color: #10b981; font-size: 0.9rem; font-weight: 600;"><i class="fas fa-check-circle"></i> Confirmation email sent to ' + email + '</p>'
                : '<p style="color: #f59e0b; font-size: 0.9rem;"><i class="fas fa-exclamation-triangle"></i> Email delivery failed. Please save this QR code.</p>';
            
            qrContainer.innerHTML = `
                <div class="qr-success">
                    <i class="fas fa-check-circle"></i>
                    <h3>Registration Successful!</h3>
                    <p>Your gate pass has been generated</p>
                    ${emailStatus}
                    <img src="${data.qr_code_image}" alt="QR Code" style="max-width: 300px; margin: 1rem auto; display: block; border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px; background: white;">
                    <p><strong>Registration ID:</strong> ${data.id}</p>
                    <p style="color: #666; font-size: 0.9rem;">
                        <i class="fas fa-info-circle"></i> This QR code is valid for single entry only
                    </p>
                    <div style="margin-top: 1rem; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                        <button onclick="downloadQR('${data.qr_code_image}', '${name}')" class="submit-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                            <i class="fas fa-download"></i> Download QR Code
                        </button>
                        <button onclick="window.print()" class="submit-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                            <i class="fas fa-print"></i> Print Pass
                        </button>
                    </div>
                </div>
            `;
            
            // Scroll to QR code
            qrContainer.scrollIntoView({ behavior: 'smooth' });
            
            // Reset form
            document.getElementById("gatePassForm").reset();
            
        } else {
            alert(`Error: ${data.error || 'Registration failed. You may already be registered for this event.'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration. Please try again.');
    }
});

// Download QR code as image
function downloadQR(qrCodeImage, name) {
    const link = document.createElement('a');
    link.href = qrCodeImage;
    link.download = `event-pass-${name.replace(/\s+/g, '-')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
