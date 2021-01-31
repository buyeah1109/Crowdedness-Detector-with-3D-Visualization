using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FloorLabelController : MonoBehaviour
{
	public GameObject cam;
	private LineRenderer lineRenderer;
	private const float sensitivity = 5f;
	private Vector2 currentRotation;
	// Start is called before the first frame update
	void Start()
	{
		currentRotation = new Vector2(cam.transform.rotation.y, cam.transform.rotation.x);
		currentRotation.x += 45f;
		currentRotation.x = Mathf.Repeat(currentRotation.x, 360);
		lineRenderer = GetComponent<LineRenderer>();
	}

	// Update is called once per frame
	void Update()
	{
		if (Input.GetButton("Fire1")) {
			currentRotation.x += Input.GetAxis("Mouse X") * sensitivity;
			currentRotation.x = Mathf.Repeat(currentRotation.x, 360);
			currentRotation.y -= Input.GetAxis("Mouse Y") * sensitivity;
			currentRotation.y = Mathf.Repeat(currentRotation.y, 360);
		}

		if (currentRotation.y > 75 && currentRotation.y < 270) {
			currentRotation.y = 75;
		}
		if (currentRotation.y >= 270 && currentRotation.y <= 360) {
			currentRotation.y = 0;
		}

		transform.rotation = Quaternion.Euler(currentRotation.y, currentRotation.x, 0);

		Vector3 pos = new Vector3(
			11.25f * Mathf.Cos(currentRotation.x / 180 * Mathf.PI),
			transform.position.y,
			-11.25f * Mathf.Sin(currentRotation.x / 180 * Mathf.PI)
		);

		Vector3 dir = new Vector3(0, transform.position.y, 0) - pos;

		Ray ray = new Ray(pos, dir);
		lineRenderer.SetPosition(0, pos);
		lineRenderer.SetPosition(1, pos + dir * 0.25f);
	}
}
