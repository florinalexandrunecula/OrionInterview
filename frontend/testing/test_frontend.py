from playwright.sync_api import Page


def test_sign_in_user(page: Page):
    page.goto("http://localhost:8501")

    page.locator("label:has-text('Sign In')").click()

    page.locator("input[aria-label='Username']").fill("testuser")
    page.locator("input[aria-label='Password']").fill("password123")
    page.locator("input[aria-label='Password']").blur()

    page.locator("button:has-text('Sign In')").click()

    page.wait_for_selector("div.stAlert:has-text('Successfully signed in!')")
    assert page.locator(
        "div.stAlert:has-text('Successfully signed in!')").is_visible()


def test_create_post(page: Page):
    page.goto("http://localhost:8501")

    page.locator("label:has-text('Sign In')").click()

    page.locator("input[aria-label='Username']").fill("testuser")
    page.locator("input[aria-label='Password']").fill("password123")

    page.locator("input[aria-label='Password']").blur()

    page.locator("button:has-text('Sign In')").click()

    page.wait_for_selector("div.stAlert:has-text('Successfully signed in!')")

    page.wait_for_timeout(3000)

    page.locator("label:has-text('Posts')").click()

    page.locator("input[aria-label='Post Title']").fill("Test Post")
    page.locator(
        "textarea[aria-label='Post Content']").fill("This is a test post content")
    page.locator("textarea[aria-label='Post Content']").blur()

    page.locator("button:has-text('Submit Post')").click()

    page.wait_for_selector(
        "div.stAlert:has-text(\"Post 'Test Post' created successfully!\")")
    assert page.locator(
        "div.stAlert:has-text(\"Post 'Test Post' created successfully!\")").is_visible()


def test_delete_post(page: Page):
    page.goto("http://localhost:8501")

    page.locator("label:has-text('Sign In')").click()

    page.locator("input[aria-label='Username']").fill("testuser")
    page.locator("input[aria-label='Password']").fill("password123")

    page.locator("input[aria-label='Password']").blur()

    page.locator("button:has-text('Sign In')").click()

    page.wait_for_selector("div.stAlert:has-text('Successfully signed in!')")

    page.wait_for_timeout(3000)

    page.locator("label:has-text('Posts')").click()

    post_title = "Test Post"
    post_locator = page.locator(f"text={post_title}").nth(0)

    post_text = post_locator.inner_text()
    post_id = post_text.split("ID: ")[1].strip(")")
    delete_button_container = page.locator(
        f"div[class*='st-key-delete_{post_id}']")
    delete_button = delete_button_container.locator(
        "button:has-text('Delete')")
    delete_button.click()

    page.wait_for_selector(
        f"div.stAlert:has-text(\"Post '{post_id}' deleted successfully!\")")
    assert page.locator(
        f"div.stAlert:has-text(\"Post '{post_id}' deleted successfully!\")").is_visible()
